# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T08:26:42.150692+00:00
- Count: 1000
- Runs: 4
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T082535Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 1890.77 | 84.46 | Postgres | 22.39x |
| Read all | 473.94 | 12.90 | Postgres | 36.74x |
| Read random 100 | 452.97 | 413.83 | Postgres | 1.09x |
| Update all | 6791.43 | 28.57 | Postgres | 237.67x |
| Update random 100 | 2150.84 | 383.42 | Postgres | 5.61x |
| Delete all | 1688.48 | 40.67 | Postgres | 41.52x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 4 | 1890.77 | 1763.75 | 2009.13 | 101.58 |
| git_read_all | 4 | 473.94 | 419.31 | 628.11 | 102.86 |
| git_read_random_100 | 4 | 452.97 | 411.44 | 509.98 | 45.76 |
| git_update_all | 4 | 6791.43 | 6546.11 | 6943.99 | 171.06 |
| git_update_random_100 | 4 | 2150.84 | 1861.95 | 2462.69 | 315.14 |
| git_delete_all | 4 | 1688.48 | 1452.33 | 1796.51 | 162.54 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 4 | 84.46 | 71.97 | 97.08 | 10.38 |
| db_read_all | 4 | 12.90 | 12.21 | 14.35 | 0.98 |
| db_read_random_100 | 4 | 413.83 | 336.83 | 558.30 | 102.34 |
| db_update_all | 4 | 28.57 | 26.74 | 30.90 | 1.95 |
| db_update_random_100 | 4 | 383.42 | 337.72 | 484.64 | 68.66 |
| db_delete_all | 4 | 40.67 | 38.81 | 43.84 | 2.22 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
