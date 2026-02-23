# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T08:50:34.336112+00:00
- Count: 15000
- Runs: 4
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T084212Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 5662.49 | 335.16 | Postgres | 16.89x |
| Read all | 604.47 | 37.66 | Postgres | 16.05x |
| Read random 100 | 512.67 | 327.29 | Postgres | 1.57x |
| Update all | 85632.81 | 175.45 | Postgres | 488.08x |
| Update random 100 | 3353.57 | 351.97 | Postgres | 9.53x |
| Delete all | 4722.64 | 45.63 | Postgres | 103.49x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 4 | 5662.49 | 5557.72 | 5927.75 | 177.25 |
| git_read_all | 4 | 604.47 | 499.61 | 883.80 | 186.42 |
| git_read_random_100 | 4 | 512.67 | 436.10 | 552.56 | 52.12 |
| git_update_all | 4 | 85632.81 | 83080.49 | 86751.05 | 1713.12 |
| git_update_random_100 | 4 | 3353.57 | 2353.66 | 6258.13 | 1936.82 |
| git_delete_all | 4 | 4722.64 | 2771.66 | 5584.80 | 1310.00 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 4 | 335.16 | 295.15 | 396.58 | 44.97 |
| db_read_all | 4 | 37.66 | 33.46 | 46.43 | 5.98 |
| db_read_random_100 | 4 | 327.29 | 315.61 | 336.38 | 10.06 |
| db_update_all | 4 | 175.45 | 152.04 | 217.65 | 29.68 |
| db_update_random_100 | 4 | 351.97 | 339.89 | 363.19 | 10.07 |
| db_delete_all | 4 | 45.63 | 41.79 | 49.51 | 3.29 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
