# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T08:08:57.419907+00:00
- Count: 100
- Runs: 5
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T080729Z
- Git data dir: git_data
- Git remote: https://gitlab.com/grumlebob-group/grumlebob-project.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 2450.69 | 59.45 | Postgres | 41.22x |
| Read all | 1682.79 | 11.43 | Postgres | 147.19x |
| Read random 100 | 1755.88 | 812.70 | Postgres | 2.16x |
| Update all | 3104.62 | 71.14 | Postgres | 43.64x |
| Update random 100 | 3205.65 | 450.97 | Postgres | 7.11x |
| Delete all | 2402.09 | 46.38 | Postgres | 51.79x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 5 | 2450.69 | 2319.57 | 2750.20 | 188.93 |
| git_read_all | 5 | 1682.79 | 1547.78 | 1948.59 | 162.14 |
| git_read_random_100 | 5 | 1755.88 | 1600.58 | 2030.57 | 198.17 |
| git_update_all | 5 | 3104.62 | 2921.45 | 3516.32 | 252.46 |
| git_update_random_100 | 5 | 3205.65 | 2933.33 | 3589.00 | 267.91 |
| git_delete_all | 5 | 2402.09 | 2345.81 | 2523.61 | 72.86 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 5 | 59.45 | 46.55 | 107.21 | 26.71 |
| db_read_all | 5 | 11.43 | 10.25 | 13.53 | 1.34 |
| db_read_random_100 | 5 | 812.70 | 363.51 | 1184.33 | 405.40 |
| db_update_all | 5 | 71.14 | 22.15 | 114.26 | 32.94 |
| db_update_random_100 | 5 | 450.97 | 332.91 | 766.75 | 178.27 |
| db_delete_all | 5 | 46.38 | 41.76 | 53.57 | 4.76 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
