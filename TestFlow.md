# Test Flow

This guide describes what the benchmark script measures, how each test is executed, and how to interpret the output.

## What We Benchmark
1. Seed: create N JSON files, commit, and push to remote Git; insert N DB rows.
2. Read all: fetch from remote Git and read every blob from the commit; DB `SELECT *`.
3. Read random 100: fetch and read 100 blobs; DB 100 point lookups.
4. Update all: change URL in all files, commit, push; DB `UPDATE` all rows.
5. Update random 100: change 100 files, commit, push; DB 100 point updates.
6. Delete all: `git rm`, commit, push; DB `TRUNCATE`.
7. Random DB operations issue one query per id to mirror per-blob access.

## Pre-Run Checklist
1. Verify `.env` contains Postgres credentials (or pass `--db-url`).
2. Ensure the database in `POSTGRES_DB` exists.
3. Verify Git remote access (`GIT_REMOTE_URL`).
4. Ensure the remote repo can accept new branches from the benchmark.
5. Decide which remote to target (GitHub vs GitLab) and set `GIT_REMOTE_URL`.
6. Decide run settings (`--count`, `--runs`, `--sample-size`).
7. For the parameter sweep, use N = 100, 1000, 15000 with runs = 4, 4, 4.

## How Each Benchmark Runs
1. Load `.env` if present and establish a Postgres connection (unless `--skip-db`).
2. Initialize a work Git repo and a bare read Git repo pointing to the remote.
3. Create a base Git commit (not timed) used for read/update/delete tests.
4. Seed runs switch to a new orphan branch to ensure an empty history.
5. Recreate the dataset so each run starts from the same state.
6. Perform the single operation (seed, read, update, delete).
7. Record elapsed time in milliseconds.
8. Repeat for the configured number of runs.
9. Report mean/min/max/stdev in `experiments\\results\\latest.md`.

## Output and Interpretation
1. Use the Summary table to compare mean timings and speedup ratios.
2. Use the Git/Postgres tables to see stability (min/max/stdev).
3. Large variance often indicates caching, compression effects, or network jitter.
4. Compare `experiments\\results\\n100_github`, `n100_gitlab`, `n1000_github`, `n1000_gitlab`, `n15000_github`, and `n15000_gitlab` to see scaling trends.
