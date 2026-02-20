# Benchmark Results

## Run Info

- Run UTC: 2026-02-20T09:19:07.714880+00:00
- Count: 1000
- Runs: 10
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260220T091540Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 1885.90 | 77.55 | Postgres | 24.32x |
| Read all | 478.07 | 15.90 | Postgres | 30.07x |
| Read random 100 | 430.08 | 363.30 | Postgres | 1.18x |
| Update all | 12018.49 | 30.51 | Postgres | 393.87x |
| Update random 100 | 2080.91 | 395.45 | Postgres | 5.26x |
| Delete all | 1536.07 | 52.76 | Postgres | 29.11x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 10 | 1885.90 | 1785.40 | 2030.05 | 70.77 |
| git_read_all | 10 | 478.07 | 403.07 | 630.48 | 75.39 |
| git_read_random_100 | 10 | 430.08 | 389.17 | 512.81 | 36.88 |
| git_update_all | 10 | 12018.49 | 6545.17 | 23719.09 | 7891.98 |
| git_update_random_100 | 10 | 2080.91 | 1761.11 | 3814.58 | 625.73 |
| git_delete_all | 10 | 1536.07 | 1415.93 | 1602.69 | 52.32 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 10 | 77.55 | 70.41 | 94.71 | 7.53 |
| db_read_all | 10 | 15.90 | 13.26 | 18.88 | 2.26 |
| db_read_random_100 | 10 | 363.30 | 340.48 | 394.19 | 18.15 |
| db_update_all | 10 | 30.51 | 26.43 | 34.03 | 2.69 |
| db_update_random_100 | 10 | 395.45 | 353.15 | 507.16 | 51.39 |
| db_delete_all | 10 | 52.76 | 43.16 | 78.61 | 9.75 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
