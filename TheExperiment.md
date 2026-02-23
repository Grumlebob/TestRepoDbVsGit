# The Experiment Plan: JSON-in-Git vs Postgres

## Goal
Demonstrate performance and operational differences between storing DataLocations as committed JSON blobs in a remote Git repo vs storing rows in a Postgres `datalocations` table across multiple dataset sizes.

## Hypothesis
Postgres will outperform Git for bulk reads and bulk updates, especially as record counts grow. Git will be simpler to version and audit, but will be slower for repeated operations when data is only accessible via remote Git objects.

## Data Model (Shared)
- `id` (int, 1..N)
- `name` (string)
- `url` (string, fake URL)

## Controls
- Dataset sizes: N = 100, 1000, 15000.
- Same machine and environment for all runs.
- Same schema for both storage types.
- Repeat each benchmark multiple runs and report mean/min/max/stdev.
- Random sample size fixed at 100 for the random read/update tests.
- Git reads use committed objects (no working tree access).

## Benchmark Matrix
| Operation | Remote Git (committed blobs) | Postgres |
| --- | --- | --- |
| Seed | Create files, commit, push | Insert N rows |
| Read all | Fetch + read blobs from commit | `SELECT *` |
| Read random (100) | Fetch + read 100 blobs | 100 point lookups |
| Update all | Modify files, commit, push | `UPDATE` all rows |
| Update random (100) | Modify 100 files, commit, push | 100 point updates |
| Delete all | `git rm`, commit, push | `TRUNCATE` table |

## Execution Steps
1. Install dependencies: `pip install -r requirements.txt`.
2. Ensure Postgres is running and connection info is available via `.env` or env vars:
   - `.env` keys: `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
   - Or `DATABASE_URL` / `Database__Host`, `Database__Name`, `Database__Username`, `Database__Password`
   - The database in `POSTGRES_DB` must already exist.
   - The benchmark script auto-loads `.env` from the repo root.
3. Ensure a remote Git repo is reachable:
   - Provide `GIT_REMOTE_URL` (HTTPS or Git server URL).
   - The remote repo should be bare or otherwise accept pushes to the target branch.
   - The benchmark creates new branches (seed/update/delete) under the chosen prefix.
   - GitHub runs use `https://github.com/Grumlebob/TestRepoDbVsGit.git` (default in `.env`).
   - GitLab runs override `GIT_REMOTE_URL` with `https://gitlab.com/grumlebob-group/grumlebob-project.git`.
4. Run the benchmark script for each parameter set (see below) and write to `_github` / `_gitlab` result directories.
5. Review results in `experiments\\results\\n100_github\\`, `experiments\\results\\n100_gitlab\\`, etc.
6. Summarize conclusions in `ProsCons.md`.

## Parameter Sweep

GitHub (default `GIT_REMOTE_URL` from `.env`):

| N | Runs | Command | Results |
| --- | --- | --- | --- |
| 100 | 4 | `python experiments\\benchmark_datalocations.py --count 100 --runs 4 --results-dir experiments\\results\\n100_github` | `experiments\\results\\n100_github\\latest.md` |
| 1000 | 4 | `python experiments\\benchmark_datalocations.py --count 1000 --runs 4 --results-dir experiments\\results\\n1000_github` | `experiments\\results\\n1000_github\\latest.md` |
| 15000 | 4 | `python experiments\\benchmark_datalocations.py --count 15000 --runs 4 --results-dir experiments\\results\\n15000_github` | `experiments\\results\\n15000_github\\latest.md` |

GitLab (override `GIT_REMOTE_URL`):

| N | Runs | Command | Results |
| --- | --- | --- | --- |
| 100 | 4 | `$env:GIT_REMOTE_URL="https://gitlab.com/grumlebob-group/grumlebob-project.git"; python experiments\\benchmark_datalocations.py --count 100 --runs 4 --results-dir experiments\\results\\n100_gitlab` | `experiments\\results\\n100_gitlab\\latest.md` |
| 1000 | 4 | `$env:GIT_REMOTE_URL="https://gitlab.com/grumlebob-group/grumlebob-project.git"; python experiments\\benchmark_datalocations.py --count 1000 --runs 4 --results-dir experiments\\results\\n1000_gitlab` | `experiments\\results\\n1000_gitlab\\latest.md` |
| 15000 | 4 | `$env:GIT_REMOTE_URL="https://gitlab.com/grumlebob-group/grumlebob-project.git"; python experiments\\benchmark_datalocations.py --count 15000 --runs 4 --results-dir experiments\\results\\n15000_gitlab` | `experiments\\results\\n15000_gitlab\\latest.md` |

## Methodology Notes
- The benchmark recreates the dataset before each run to keep runs comparable.
- Git reads fetch the remote and read committed blobs (no working tree).
- A base Git commit is created once and reused for read/update/delete tests.
- Seed tests create new orphan branches (empty history) for each run.
- Update/delete tests create new branches from the base commit and push those changes.
- Random samples are generated once per run using a fixed seed.
- DB tests keep one connection open (no connection setup time included).
- Random DB tests issue one query per id to mirror per-blob access.

## Threats to Validity
- Network latency to the Git or DB host can dominate random access timings.
- Git fetch behavior depends on object reuse and compression.
- Results vary by hardware, OS, and storage type (SSD vs HDD).

## Optional Variations
- Add `--fsync` to measure durable file writes before commit.
- Add a batched DB random benchmark using `WHERE id IN (...)`.
- Increase `--count` to observe scaling behavior.

## Output Artifacts
- `experiments\\results\\n100_github\\latest.json`
- `experiments\\results\\n100_github\\latest.md`
- `experiments\\results\\n100_gitlab\\latest.json`
- `experiments\\results\\n100_gitlab\\latest.md`
- `experiments\\results\\n1000_github\\latest.json`
- `experiments\\results\\n1000_github\\latest.md`
- `experiments\\results\\n1000_gitlab\\latest.json`
- `experiments\\results\\n1000_gitlab\\latest.md`
- `experiments\\results\\n15000_github\\latest.json`
- `experiments\\results\\n15000_github\\latest.md`
- `experiments\\results\\n15000_gitlab\\latest.json`
- `experiments\\results\\n15000_gitlab\\latest.md`
- `experiments\\results\\latest.json` (copy of the most recent run)
- `experiments\\results\\latest.md` (copy of the most recent run)
- `ProsCons.md`
- `experiments\\git_work\\` and `experiments\\git_read\\` (local Git clones used for benchmarks)

## Success Criteria
- Benchmark timings recorded for each operation in both storage types for GitHub and GitLab remotes.
- Pros/Cons written with references to measured results.
