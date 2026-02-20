from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import stat
import statistics
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Callable, Iterable, List, Optional
from urllib.parse import urlparse

try:
    import psycopg
except ImportError:  # pragma: no cover - handled in main
    psycopg = None


TABLE_NAME_DEFAULT = "DataLocations"
GIT_DATA_DIR_DEFAULT = "git_data"
GIT_REMOTE_NAME = "origin"
GIT_BRANCH_DEFAULT = "main"
DEFAULT_GIT_USER_NAME = "Benchmark Bot"
DEFAULT_GIT_USER_EMAIL = "benchmark@example.com"


@dataclass
class BenchmarkResult:
    name: str
    runs: int
    times_s: List[float]
    mean_ms: float
    min_ms: float
    max_ms: float
    stdev_ms: float


def _safe_table_name(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        raise ValueError(f"Unsafe table name: {name!r}")
    return f"\"{name}\""


def _redact_dsn(dsn: str) -> str:
    if "://" not in dsn:
        return "<provided>"
    parsed = urlparse(dsn)
    netloc = parsed.netloc
    if "@" in netloc:
        creds, host = netloc.split("@", 1)
        user = creds.split(":", 1)[0]
        netloc = f"{user}:****@{host}"
    return parsed._replace(netloc=netloc).geturl()


def _redact_remote(remote: str) -> str:
    if "://" in remote:
        parsed = urlparse(remote)
        netloc = parsed.netloc
        if "@" in netloc:
            creds, host = netloc.split("@", 1)
            if ":" in creds:
                user = creds.split(":", 1)[0]
                netloc = f"{user}:****@{host}"
        return parsed._replace(netloc=netloc).geturl()
    if "@" in remote and ":" in remote.split("@", 1)[0]:
        creds, host = remote.split("@", 1)
        user = creds.split(":", 1)[0]
        return f"{user}:****@{host}"
    return remote


def _write_json(path: Path, payload: dict, fsync: bool) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        if fsync:
            handle.flush()
            os.fsync(handle.fileno())


def _read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _record_for(idx: int, base_url: str) -> dict:
    return {
        "id": idx,
        "name": f"Location {idx}",
        "url": f"{base_url}/{idx}",
    }


def _decode_bytes(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def _run_git(
    repo: Optional[Path],
    args: List[str],
    input_data: Optional[bytes] = None,
    text: bool = True,
) -> str | bytes:
    cmd = ["git"]
    if repo is not None:
        cmd.extend(["-C", str(repo)])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )
    if result.returncode != 0:
        stdout = result.stdout if isinstance(result.stdout, str) else _decode_bytes(result.stdout)
        stderr = result.stderr if isinstance(result.stderr, str) else _decode_bytes(result.stderr)
        details = stderr.strip() or stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {details}")
    return result.stdout


def _remove_readonly(func, path, _excinfo) -> None:
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except OSError:
        pass


def _ensure_empty_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, onerror=_remove_readonly)
    path.mkdir(parents=True, exist_ok=True)


def git_init_repo(path: Path, branch: str, bare: bool) -> None:
    _ensure_empty_dir(path)
    if bare:
        _run_git(path, ["init", "--bare"])
        _run_git(path, ["symbolic-ref", "HEAD", f"refs/heads/{branch}"])
    else:
        _run_git(path, ["init", "-b", branch])


def git_config_user(repo: Path, name: str, email: str) -> None:
    _run_git(repo, ["config", "user.name", name])
    _run_git(repo, ["config", "user.email", email])


def git_clean_repo(repo: Path) -> None:
    _run_git(repo, ["reset", "--hard"])
    _run_git(repo, ["clean", "-fdx"])


def git_checkout_orphan(repo: Path, branch: str) -> None:
    _run_git(repo, ["checkout", "--orphan", branch])
    _run_git(repo, ["rm", "-rf", "--ignore-unmatch", "."])
    _run_git(repo, ["clean", "-fdx"])


def git_checkout_branch_from(repo: Path, branch: str, start_point: str) -> None:
    _run_git(repo, ["checkout", "-B", branch, start_point])
    _run_git(repo, ["reset", "--hard"])
    _run_git(repo, ["clean", "-fdx"])


def git_set_remote(repo: Path, remote_url: str) -> None:
    remotes = _run_git(repo, ["remote"], text=True).splitlines()
    if GIT_REMOTE_NAME in remotes:
        _run_git(repo, ["remote", "set-url", GIT_REMOTE_NAME, remote_url])
    else:
        _run_git(repo, ["remote", "add", GIT_REMOTE_NAME, remote_url])


def git_check_remote(remote_url: str) -> None:
    _run_git(None, ["ls-remote", "--heads", remote_url], text=True)


def git_rev_parse(repo: Path, ref: str) -> str:
    return _run_git(repo, ["rev-parse", ref], text=True).strip()


def git_fetch(repo: Path, branch: str) -> None:
    _run_git(repo, ["fetch", "--prune", GIT_REMOTE_NAME, branch])


def git_tree_blobs(repo: Path, commit: str, data_dir: str) -> dict[str, str]:
    output = _run_git(repo, ["ls-tree", "-r", "-z", commit, data_dir], text=False)
    entries = output.split(b"\0")
    mapping: dict[str, str] = {}
    for entry in entries:
        if not entry:
            continue
        header, path = entry.split(b"\t", 1)
        parts = _decode_bytes(header).split()
        if len(parts) < 3:
            continue
        mapping[_decode_bytes(path)] = parts[2]
    return mapping


def git_read_blobs(repo: Path, object_ids: List[str]) -> None:
    if not object_ids:
        return
    input_data = ("\n".join(object_ids) + "\n").encode("utf-8")
    output = _run_git(repo, ["cat-file", "--batch"], input_data=input_data, text=False)
    offset = 0
    for _obj_id in object_ids:
        header_end = output.index(b"\n", offset)
        header = _decode_bytes(output[offset:header_end])
        header_parts = header.split()
        if len(header_parts) == 2 and header_parts[1] == "missing":
            raise RuntimeError(f"Missing git object: {header_parts[0]}")
        size = int(header_parts[2])
        content_start = header_end + 1
        content_end = content_start + size
        payload = output[content_start:content_end]
        json.loads(payload.decode("utf-8"))
        offset = content_end + 1


def git_read_all(repo: Path, commit: str, data_dir: str) -> None:
    blob_map = git_tree_blobs(repo, commit, data_dir)
    git_read_blobs(repo, list(blob_map.values()))


def git_read_random(repo: Path, commit: str, data_dir: str, sample_ids: Iterable[int]) -> None:
    blob_map = git_tree_blobs(repo, commit, data_dir)
    object_ids: List[str] = []
    for idx in sample_ids:
        path = f"{data_dir}/{idx}.json"
        object_id = blob_map.get(path)
        if not object_id:
            raise RuntimeError(f"Missing blob for {path}")
        object_ids.append(object_id)
    git_read_blobs(repo, object_ids)


def git_prepare_dataset(
    repo: Path, data_dir: str, count: int, base_url: str, fsync: bool
) -> None:
    data_path = repo / data_dir
    if data_path.exists():
        shutil.rmtree(data_path)
    data_path.mkdir(parents=True, exist_ok=True)
    for idx in range(1, count + 1):
        _write_json(data_path / f"{idx}.json", _record_for(idx, base_url), fsync)


def git_update_all(
    repo: Path, data_dir: str, count: int, base_url: str, run_idx: int, fsync: bool
) -> None:
    for idx in range(1, count + 1):
        path = repo / data_dir / f"{idx}.json"
        payload = _read_json(path)
        payload["url"] = f"{base_url}/updated?run={run_idx}"
        _write_json(path, payload, fsync)


def git_update_random(
    repo: Path, data_dir: str, sample_ids: Iterable[int], base_url: str, run_idx: int, fsync: bool
) -> None:
    for idx in sample_ids:
        path = repo / data_dir / f"{idx}.json"
        payload = _read_json(path)
        payload["url"] = f"{base_url}/updated/{idx}?run={run_idx}"
        _write_json(path, payload, fsync)


def git_delete_all(repo: Path, data_dir: str) -> None:
    data_path = repo / data_dir
    if data_path.exists():
        shutil.rmtree(data_path)


def git_commit_push(repo: Path, branch: str, message: str) -> None:
    _run_git(repo, ["add", "-A"])
    status = _run_git(repo, ["status", "--porcelain"], text=True).strip()
    if not status:
        raise RuntimeError("No changes to commit for git benchmark.")
    _run_git(repo, ["commit", "-m", message])
    _run_git(repo, ["push", GIT_REMOTE_NAME, f"HEAD:{branch}"])


def git_seed(
    repo: Path, data_dir: str, count: int, base_url: str, fsync: bool, branch: str
) -> str:
    git_prepare_dataset(repo, data_dir, count, base_url, fsync)
    git_commit_push(repo, branch, f"seed {count}")
    return git_rev_parse(repo, "HEAD")


def git_update_all_commit(
    repo: Path, data_dir: str, count: int, base_url: str, run_idx: int, fsync: bool, branch: str
) -> None:
    git_update_all(repo, data_dir, count, base_url, run_idx, fsync)
    git_commit_push(repo, branch, f"update all run {run_idx}")


def git_update_random_commit(
    repo: Path,
    data_dir: str,
    sample_ids: Iterable[int],
    base_url: str,
    run_idx: int,
    fsync: bool,
    branch: str,
) -> None:
    git_update_random(repo, data_dir, sample_ids, base_url, run_idx, fsync)
    git_commit_push(repo, branch, f"update random run {run_idx}")


def git_delete_all_commit(repo: Path, data_dir: str, branch: str) -> None:
    git_delete_all(repo, data_dir)
    git_commit_push(repo, branch, "delete all")


def _db_connect(dsn: str):
    if psycopg is None:
        raise RuntimeError("psycopg is not installed. Run: pip install -r requirements.txt")
    return psycopg.connect(dsn)


def _db_ensure_table(conn, table: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL
            )
            """
        )
    conn.commit()


def seed_db(conn, table: str, count: int, base_url: str) -> None:
    rows = [(idx, f"Location {idx}", f"{base_url}/{idx}") for idx in range(1, count + 1)]
    with conn.cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {table}")
        cur.executemany(f"INSERT INTO {table} (id, name, url) VALUES (%s, %s, %s)", rows)
    conn.commit()


def read_all_db(conn, table: str) -> None:
    with conn.cursor() as cur:
        cur.execute(f"SELECT id, name, url FROM {table} ORDER BY id")
        cur.fetchall()


def read_random_db(conn, table: str, sample_ids: Iterable[int]) -> None:
    with conn.cursor() as cur:
        for idx in sample_ids:
            cur.execute(f"SELECT id, name, url FROM {table} WHERE id = %s", (idx,))
            cur.fetchone()


def update_all_db(conn, table: str, new_url: str) -> None:
    with conn.cursor() as cur:
        cur.execute(f"UPDATE {table} SET url = %s", (new_url,))
    conn.commit()


def update_random_db(
    conn, table: str, sample_ids: Iterable[int], base_url: str, run_idx: int
) -> None:
    with conn.cursor() as cur:
        for idx in sample_ids:
            cur.execute(
                f"UPDATE {table} SET url = %s WHERE id = %s",
                (f"{base_url}/updated/{idx}?run={run_idx}", idx),
            )
    conn.commit()


def delete_all_db(conn, table: str) -> None:
    with conn.cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {table}")
    conn.commit()


def drop_table(conn, table: str) -> None:
    with conn.cursor() as cur:
        cur.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()


def run_benchmark(
    name: str,
    fn: Callable[[int], None],
    runs: int,
    setup: Optional[Callable[[int], None]] = None,
    teardown: Optional[Callable[[int], None]] = None,
) -> BenchmarkResult:
    times: List[float] = []
    for run_idx in range(runs):
        if setup:
            setup(run_idx)
        start = perf_counter()
        fn(run_idx)
        end = perf_counter()
        if teardown:
            teardown(run_idx)
        times.append(end - start)
    mean_s = statistics.mean(times)
    stdev_s = statistics.stdev(times) if len(times) > 1 else 0.0
    return BenchmarkResult(
        name=name,
        runs=runs,
        times_s=times,
        mean_ms=mean_s * 1000.0,
        min_ms=min(times) * 1000.0,
        max_ms=max(times) * 1000.0,
        stdev_ms=stdev_s * 1000.0,
    )


def build_dsn(args: argparse.Namespace) -> str:
    if args.db_url:
        return args.db_url
    if os.getenv("DATABASE_URL"):
        return os.environ["DATABASE_URL"]
    if os.getenv("POSTGRES_HOST"):
        host = os.environ["POSTGRES_HOST"]
        name = os.environ.get("POSTGRES_DB", "postgres")
        user = os.environ.get("POSTGRES_USER", "postgres")
        password = os.environ.get("POSTGRES_PASSWORD", "")
        port = os.environ.get("POSTGRES_PORT", "5432")
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"
    if os.getenv("Database__Host"):
        host = os.environ["Database__Host"]
        name = os.environ.get("Database__Name", "postgres")
        user = os.environ.get("Database__Username", "postgres")
        password = os.environ.get("Database__Password", "")
        port = os.environ.get("Database__Port", "5432")
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"
    raise RuntimeError(
        "No database connection info found. Set --db-url or DATABASE_URL or Database__Host/Name/Username/Password."
    )


def build_git_remote(args: argparse.Namespace) -> str:
    if args.git_remote_url:
        return args.git_remote_url
    if os.getenv("GIT_REMOTE_URL"):
        return os.environ["GIT_REMOTE_URL"]
    raise RuntimeError(
        "No git remote configured. Set --git-remote-url or GIT_REMOTE_URL."
    )


def write_results(results_dir: Path, meta: dict, results: List[BenchmarkResult]) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    results_map = {result.name: result for result in results}
    operations = [
        ("Seed", "git_seed", "db_seed"),
        ("Read all", "git_read_all", "db_read_all"),
        ("Read random 100", "git_read_random_100", "db_read_random_100"),
        ("Update all", "git_update_all", "db_update_all"),
        ("Update random 100", "git_update_random_100", "db_update_random_100"),
        ("Delete all", "git_delete_all", "db_delete_all"),
    ]

    def _table(headers: List[str], rows: List[List[str]]) -> List[str]:
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
        ]
        for row in rows:
            lines.append("| " + " | ".join(row) + " |")
        return lines

    def _speedup(git_ms: float, db_ms: float) -> tuple[str, str]:
        if git_ms == db_ms:
            return "Tie", "1.00x"
        faster = "Git" if git_ms < db_ms else "Postgres"
        ratio = max(git_ms, db_ms) / min(git_ms, db_ms)
        return faster, f"{ratio:.2f}x"

    json_payload = {
        "meta": meta,
        "results": [
            {
                "name": result.name,
                "runs": result.runs,
                "mean_ms": result.mean_ms,
                "min_ms": result.min_ms,
                "max_ms": result.max_ms,
                "stdev_ms": result.stdev_ms,
            }
            for result in results
        ],
    }
    (results_dir / "latest.json").write_text(
        json.dumps(json_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    lines = [
        "# Benchmark Results",
        "",
        "## Run Info",
        "",
        f"- Run UTC: {meta['run_utc']}",
        f"- Count: {meta['count']}",
        f"- Runs: {meta['runs']}",
        f"- Sample size: {meta['sample_size']}",
        f"- Table: {meta['table_name']}",
        f"- Git branch: {meta.get('git_branch')}",
        f"- Git data dir: {meta.get('git_data_dir')}",
        f"- Git remote: {meta.get('git_remote')}",
        "",
    ]

    summary_rows: List[List[str]] = []
    for label, git_key, db_key in operations:
        git_result = results_map.get(git_key)
        db_result = results_map.get(db_key)
        if git_result and db_result:
            faster, ratio = _speedup(git_result.mean_ms, db_result.mean_ms)
            summary_rows.append(
                [
                    label,
                    f"{git_result.mean_ms:.2f}",
                    f"{db_result.mean_ms:.2f}",
                    faster,
                    ratio,
                ]
            )
    if summary_rows:
        lines.extend(
            [
                "## Summary (Mean ms)",
                "",
                *_table(
                    ["Operation", "Git (remote)", "Postgres", "Faster", "Speedup"],
                    summary_rows,
                ),
                "",
            ]
        )

    git_rows = []
    for key in [name for name in results_map if name.startswith("git_")]:
        result = results_map[key]
        git_rows.append(
            [
                key,
                str(result.runs),
                f"{result.mean_ms:.2f}",
                f"{result.min_ms:.2f}",
                f"{result.max_ms:.2f}",
                f"{result.stdev_ms:.2f}",
            ]
        )
    if git_rows:
        lines.extend(
            [
                "## Git Benchmarks",
                "",
                *_table(
                    ["Benchmark", "Runs", "Mean (ms)", "Min (ms)", "Max (ms)", "Stdev (ms)"],
                    git_rows,
                ),
                "",
            ]
        )

    db_rows = []
    for key in [name for name in results_map if name.startswith("db_")]:
        result = results_map[key]
        db_rows.append(
            [
                key,
                str(result.runs),
                f"{result.mean_ms:.2f}",
                f"{result.min_ms:.2f}",
                f"{result.max_ms:.2f}",
                f"{result.stdev_ms:.2f}",
            ]
        )
    if db_rows:
        lines.extend(
            [
                "## Postgres Benchmarks",
                "",
                *_table(
                    ["Benchmark", "Runs", "Mean (ms)", "Min (ms)", "Max (ms)", "Stdev (ms)"],
                    db_rows,
                ),
                "",
            ]
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).")
    lines.append("- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.")
    lines.append("- Connection setup is excluded; DB connection stays open during benchmarks.")
    lines.append("- Speedup is the ratio of slower to faster (higher means bigger gap).")
    (results_dir / "latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    default_results_dir = root / "experiments" / "results"
    default_git_work_dir = root / "experiments" / "git_work"
    default_git_read_dir = root / "experiments" / "git_read"

    parser = argparse.ArgumentParser(
        description="Benchmark remote Git (committed JSON) vs Postgres for DataLocations."
    )
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--sample-size", type=int, default=100)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--base-url", default="https://example.com/resource")
    parser.add_argument("--results-dir", default=str(default_results_dir))
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--table-name", default=TABLE_NAME_DEFAULT)
    parser.add_argument("--git-remote-url", default=None)
    parser.add_argument("--git-branch", default=GIT_BRANCH_DEFAULT)
    parser.add_argument("--git-data-dir", default=GIT_DATA_DIR_DEFAULT)
    parser.add_argument("--git-work-dir", default=str(default_git_work_dir))
    parser.add_argument("--git-read-dir", default=str(default_git_read_dir))
    parser.add_argument("--git-user-name", default=None)
    parser.add_argument("--git-user-email", default=None)
    parser.add_argument("--skip-git", action="store_true")
    parser.add_argument("--skip-files", action="store_true", help="Deprecated: use --skip-git")
    parser.add_argument("--skip-db", action="store_true")
    parser.add_argument("--drop-table", action="store_true")
    parser.add_argument("--fsync", action="store_true")
    parser.add_argument("--cleanup-git", action="store_true")
    return parser.parse_args()


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key in os.environ:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        os.environ[key] = value


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    load_env_file(root / ".env")
    args = parse_args()
    if args.count <= 0:
        raise ValueError("--count must be > 0")
    if args.runs <= 0:
        raise ValueError("--runs must be > 0")
    if args.sample_size <= 0:
        raise ValueError("--sample-size must be > 0")

    random.seed(args.seed)

    count = args.count
    sample_size = min(args.sample_size, count)
    sample_sets = [
        random.sample(range(1, count + 1), sample_size) for _ in range(args.runs)
    ]

    results_dir = Path(args.results_dir)
    results: List[BenchmarkResult] = []

    skip_git = args.skip_git or args.skip_files

    conn = None
    table = _safe_table_name(args.table_name)
    dsn = None

    git_remote = None
    git_branch = args.git_branch
    git_data_dir = args.git_data_dir
    git_work_dir = Path(args.git_work_dir)
    git_read_dir = Path(args.git_read_dir)
    git_user_name = args.git_user_name or os.getenv("GIT_USER_NAME", DEFAULT_GIT_USER_NAME)
    git_user_email = args.git_user_email or os.getenv("GIT_USER_EMAIL", DEFAULT_GIT_USER_EMAIL)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if not skip_git:
        git_remote = build_git_remote(args)
        git_check_remote(git_remote)
        git_init_repo(git_work_dir, git_branch, bare=False)
        git_config_user(git_work_dir, git_user_name, git_user_email)
        git_set_remote(git_work_dir, git_remote)
        git_init_repo(git_read_dir, git_branch, bare=True)
        git_set_remote(git_read_dir, git_remote)

    if not args.skip_db:
        dsn = build_dsn(args)
        conn = _db_connect(dsn)
        _db_ensure_table(conn, table)

    if not skip_git:
        seed_branch_prefix = f"{git_branch}-seed-{run_id}"
        base_branch = f"{git_branch}-base-{run_id}"
        seed_branches: List[Optional[str]] = [None] * args.runs

        git_checkout_orphan(git_work_dir, base_branch)
        base_commit = git_seed(
            git_work_dir, git_data_dir, count, args.base_url, args.fsync, base_branch
        )

        def seed_setup(run_idx: int) -> None:
            branch = f"{seed_branch_prefix}-{run_idx + 1}"
            seed_branches[run_idx] = branch
            git_checkout_orphan(git_work_dir, branch)

        def seed_run(run_idx: int) -> None:
            branch = seed_branches[run_idx]
            if not branch:
                raise RuntimeError("Missing seed branch for run.")
            git_seed(git_work_dir, git_data_dir, count, args.base_url, args.fsync, branch)

        def git_read_all_run(_run_idx: int) -> None:
            git_fetch(git_read_dir, base_branch)
            git_read_all(git_read_dir, base_commit, git_data_dir)

        def git_read_random_run(run_idx: int) -> None:
            git_fetch(git_read_dir, base_branch)
            git_read_random(git_read_dir, base_commit, git_data_dir, sample_sets[run_idx])

        def git_update_all_run(run_idx: int) -> None:
            branch = f"{git_branch}-update-all-{run_id}-{run_idx + 1}"
            git_checkout_branch_from(git_work_dir, branch, base_commit)
            git_update_all_commit(
                git_work_dir, git_data_dir, count, args.base_url, run_idx, args.fsync, branch
            )

        def git_update_random_run(run_idx: int) -> None:
            branch = f"{git_branch}-update-random-{run_id}-{run_idx + 1}"
            git_checkout_branch_from(git_work_dir, branch, base_commit)
            git_update_random_commit(
                git_work_dir,
                git_data_dir,
                sample_sets[run_idx],
                args.base_url,
                run_idx,
                args.fsync,
                branch,
            )

        def git_delete_all_run(run_idx: int) -> None:
            branch = f"{git_branch}-delete-all-{run_id}-{run_idx + 1}"
            git_checkout_branch_from(git_work_dir, branch, base_commit)
            git_delete_all_commit(git_work_dir, git_data_dir, branch)

        results.append(run_benchmark("git_seed", seed_run, args.runs, setup=seed_setup))
        results.append(run_benchmark("git_read_all", git_read_all_run, args.runs))
        results.append(run_benchmark("git_read_random_100", git_read_random_run, args.runs))
        results.append(run_benchmark("git_update_all", git_update_all_run, args.runs))
        results.append(run_benchmark("git_update_random_100", git_update_random_run, args.runs))
        results.append(run_benchmark("git_delete_all", git_delete_all_run, args.runs))

    if not args.skip_db and conn is not None:
        results.append(
            run_benchmark(
                "db_seed",
                lambda _run: seed_db(conn, table, count, args.base_url),
                args.runs,
            )
        )
        results.append(
            run_benchmark(
                "db_read_all",
                lambda _run: read_all_db(conn, table),
                args.runs,
                setup=lambda _run: seed_db(conn, table, count, args.base_url),
            )
        )
        results.append(
            run_benchmark(
                "db_read_random_100",
                lambda run_idx: read_random_db(conn, table, sample_sets[run_idx]),
                args.runs,
                setup=lambda _run: seed_db(conn, table, count, args.base_url),
            )
        )
        results.append(
            run_benchmark(
                "db_update_all",
                lambda run_idx: update_all_db(
                    conn, table, f"{args.base_url}/updated?run={run_idx}"
                ),
                args.runs,
                setup=lambda _run: seed_db(conn, table, count, args.base_url),
            )
        )
        results.append(
            run_benchmark(
                "db_update_random_100",
                lambda run_idx: update_random_db(
                    conn, table, sample_sets[run_idx], args.base_url, run_idx
                ),
                args.runs,
                setup=lambda _run: seed_db(conn, table, count, args.base_url),
            )
        )
        results.append(
            run_benchmark(
                "db_delete_all",
                lambda _run: delete_all_db(conn, table),
                args.runs,
                setup=lambda _run: seed_db(conn, table, count, args.base_url),
            )
        )
        if args.drop_table:
            drop_table(conn, table)
        conn.close()

    if args.cleanup_git and not skip_git:
        if git_work_dir.exists():
            shutil.rmtree(git_work_dir)
        if git_read_dir.exists():
            shutil.rmtree(git_read_dir)

    meta = {
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "count": count,
        "runs": args.runs,
        "sample_size": sample_size,
        "db_dsn": _redact_dsn(dsn) if dsn else None,
        "table_name": args.table_name,
        "git_remote": _redact_remote(git_remote) if git_remote else None,
        "git_branch": base_branch if (git_remote and not skip_git) else None,
        "git_data_dir": git_data_dir if git_remote else None,
        "git_run_id": run_id if (git_remote and not skip_git) else None,
    }
    write_results(results_dir, meta, results)
    print(f"Wrote results to {results_dir / 'latest.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
