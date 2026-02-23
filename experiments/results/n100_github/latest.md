# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T08:20:40.224290+00:00
- Count: 100
- Runs: 4
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T081948Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 1253.30 | 53.93 | Postgres | 23.24x |
| Read all | 497.58 | 11.73 | Postgres | 42.43x |
| Read random 100 | 427.96 | 419.62 | Postgres | 1.02x |
| Update all | 3635.68 | 19.65 | Postgres | 185.03x |
| Update random 100 | 3547.51 | 382.70 | Postgres | 9.27x |
| Delete all | 1294.57 | 44.68 | Postgres | 28.97x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 4 | 1253.30 | 1207.40 | 1296.33 | 38.15 |
| git_read_all | 4 | 497.58 | 406.74 | 626.36 | 103.23 |
| git_read_random_100 | 4 | 427.96 | 404.77 | 477.86 | 33.77 |
| git_update_all | 4 | 3635.68 | 3555.98 | 3672.99 | 54.34 |
| git_update_random_100 | 4 | 3547.51 | 3488.91 | 3597.53 | 51.52 |
| git_delete_all | 4 | 1294.57 | 1260.28 | 1320.21 | 24.98 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 4 | 53.93 | 44.49 | 75.99 | 14.84 |
| db_read_all | 4 | 11.73 | 10.39 | 12.97 | 1.32 |
| db_read_random_100 | 4 | 419.62 | 363.41 | 526.70 | 74.18 |
| db_update_all | 4 | 19.65 | 16.61 | 23.95 | 3.14 |
| db_update_random_100 | 4 | 382.70 | 355.10 | 423.10 | 28.81 |
| db_delete_all | 4 | 44.68 | 33.38 | 51.46 | 7.90 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
