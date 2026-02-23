# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T08:39:00.380307+00:00
- Count: 15000
- Runs: 4
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T083158Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 6107.23 | 358.07 | Postgres | 17.06x |
| Read all | 628.02 | 37.66 | Postgres | 16.68x |
| Read random 100 | 487.96 | 356.60 | Postgres | 1.37x |
| Update all | 83069.84 | 186.79 | Postgres | 444.73x |
| Update random 100 | 3324.94 | 370.80 | Postgres | 8.97x |
| Delete all | 4663.10 | 44.47 | Postgres | 104.87x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 4 | 6107.23 | 5936.31 | 6221.85 | 122.62 |
| git_read_all | 4 | 628.02 | 520.18 | 914.52 | 191.21 |
| git_read_random_100 | 4 | 487.96 | 424.67 | 597.57 | 77.40 |
| git_update_all | 4 | 83069.84 | 80813.53 | 84114.79 | 1519.72 |
| git_update_random_100 | 4 | 3324.94 | 2359.90 | 6138.37 | 1875.72 |
| git_delete_all | 4 | 4663.10 | 2875.08 | 5322.19 | 1194.10 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 4 | 358.07 | 305.62 | 404.49 | 50.65 |
| db_read_all | 4 | 37.66 | 30.93 | 46.90 | 7.74 |
| db_read_random_100 | 4 | 356.60 | 328.20 | 416.11 | 40.37 |
| db_update_all | 4 | 186.79 | 180.49 | 202.63 | 10.65 |
| db_update_random_100 | 4 | 370.80 | 353.18 | 409.87 | 26.25 |
| db_delete_all | 4 | 44.47 | 38.31 | 47.65 | 4.39 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
