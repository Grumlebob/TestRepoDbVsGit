# The Experiment Plan: JSON-in-Git vs Postgres

## Goal
Demonstrate performance and operational differences between storing 1,000 DataLocations as committed JSON blobs in a remote Git repo vs storing 1,000 rows in a Postgres `datalocations` table.

## Hypothesis
Postgres will outperform Git for bulk reads and bulk updates, especially as record counts grow. Git will be simpler to version and audit, but will be slower for repeated operations when data is only accessible via remote Git objects.

## Data Model (Shared)
- `id` (int, 1..1000)
- `name` (string)
- `url` (string, fake URL)

## Controls
- Fixed dataset size: 1,000 records.
- Same machine and environment for all runs.
- Same schema for both storage types.
- Repeat each benchmark multiple runs and report mean/min/max/stdev.
- Random sample size fixed at 100 for the random read/update tests.
- Git reads use committed objects (no working tree access).

## Benchmark Matrix
| Operation | Remote Git (committed blobs) | Postgres |
| --- | --- | --- |
| Seed | Create files, commit, push | Insert 1,000 rows |
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
4. Run the benchmark script:
   `python experiments\\benchmark_datalocations.py --count 1000 --runs 5`
5. Review results in `experiments\\results\\latest.md` and `experiments\\results\\latest.json`.
6. Summarize conclusions in `ProsCons.md`.

## Latest Run (for reference)
- `python experiments\\benchmark_datalocations.py --count 1500 --runs 20`
- Results: `experiments\\results\\latest.md`

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
- `experiments\\results\\latest.json`
- `experiments\\results\\latest.md`
- `ProsCons.md`
- `experiments\\git_work\\` and `experiments\\git_read\\` (local Git clones used for benchmarks)

## Success Criteria
- Benchmark timings recorded for each operation in both storage types.
- Pros/Cons written with references to measured results.
