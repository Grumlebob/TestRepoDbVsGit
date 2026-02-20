# Benchmark Results

## Run Info

- Run UTC: 2026-02-20T10:36:07.742029+00:00
- Count: 15000
- Runs: 3
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260220T102956Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 5697.33 | 342.00 | Postgres | 16.66x |
| Read all | 720.06 | 42.51 | Postgres | 16.94x |
| Read random 100 | 421.52 | 348.95 | Postgres | 1.21x |
| Update all | 99237.96 | 234.42 | Postgres | 423.34x |
| Update random 100 | 3654.75 | 388.69 | Postgres | 9.40x |
| Delete all | 4547.86 | 54.20 | Postgres | 83.90x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 3 | 5697.33 | 5541.27 | 5923.02 | 200.18 |
| git_read_all | 3 | 720.06 | 494.53 | 1150.53 | 372.94 |
| git_read_random_100 | 3 | 421.52 | 397.14 | 436.76 | 21.33 |
| git_update_all | 3 | 99237.96 | 79047.28 | 136072.39 | 31948.81 |
| git_update_random_100 | 3 | 3654.75 | 2390.45 | 6089.74 | 2109.28 |
| git_delete_all | 3 | 4547.86 | 2741.93 | 5521.25 | 1565.57 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 3 | 342.00 | 269.03 | 416.30 | 73.64 |
| db_read_all | 3 | 42.51 | 36.86 | 51.71 | 8.03 |
| db_read_random_100 | 3 | 348.95 | 340.61 | 357.08 | 8.24 |
| db_update_all | 3 | 234.42 | 173.02 | 340.11 | 91.93 |
| db_update_random_100 | 3 | 388.69 | 351.95 | 413.76 | 32.51 |
| db_delete_all | 3 | 54.20 | 50.56 | 57.94 | 3.69 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
