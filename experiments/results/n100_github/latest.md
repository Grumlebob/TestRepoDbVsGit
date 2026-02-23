# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T08:40:59.805903+00:00
- Count: 100
- Runs: 4
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T084024Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 1210.91 | 56.59 | Postgres | 21.40x |
| Read all | 481.64 | 11.33 | Postgres | 42.52x |
| Read random 100 | 411.86 | 392.64 | Postgres | 1.05x |
| Update all | 1793.83 | 20.95 | Postgres | 85.60x |
| Update random 100 | 1813.75 | 349.82 | Postgres | 5.18x |
| Delete all | 1255.81 | 38.99 | Postgres | 32.21x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 4 | 1210.91 | 1177.51 | 1241.77 | 28.03 |
| git_read_all | 4 | 481.64 | 388.19 | 591.12 | 97.24 |
| git_read_random_100 | 4 | 411.86 | 408.43 | 419.02 | 4.84 |
| git_update_all | 4 | 1793.83 | 1746.33 | 1839.82 | 38.64 |
| git_update_random_100 | 4 | 1813.75 | 1783.00 | 1897.71 | 56.02 |
| git_delete_all | 4 | 1255.81 | 1217.89 | 1287.18 | 28.87 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 4 | 56.59 | 45.49 | 79.78 | 15.66 |
| db_read_all | 4 | 11.33 | 10.15 | 12.71 | 1.12 |
| db_read_random_100 | 4 | 392.64 | 322.95 | 551.18 | 106.44 |
| db_update_all | 4 | 20.95 | 19.40 | 23.10 | 1.68 |
| db_update_random_100 | 4 | 349.82 | 338.19 | 363.58 | 11.18 |
| db_delete_all | 4 | 38.99 | 31.01 | 48.13 | 7.47 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
