# Benchmark Results

## Run Info

- Run UTC: 2026-02-20T08:42:35.252162+00:00
- Count: 1000
- Runs: 5
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260220T084113Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 1885.52 | 71.30 | Postgres | 26.45x |
| Read all | 513.90 | 12.15 | Postgres | 42.31x |
| Read random 100 | 460.95 | 349.58 | Postgres | 1.32x |
| Update all | 7004.18 | 27.29 | Postgres | 256.62x |
| Update random 100 | 2007.47 | 373.05 | Postgres | 5.38x |
| Delete all | 1584.57 | 43.32 | Postgres | 36.57x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 5 | 1885.52 | 1785.23 | 1981.63 | 80.69 |
| git_read_all | 5 | 513.90 | 409.89 | 617.33 | 73.60 |
| git_read_random_100 | 5 | 460.95 | 414.08 | 511.53 | 43.38 |
| git_update_all | 5 | 7004.18 | 6675.12 | 7184.35 | 214.57 |
| git_update_random_100 | 5 | 2007.47 | 1819.57 | 2349.97 | 222.91 |
| git_delete_all | 5 | 1584.57 | 1393.78 | 1669.00 | 109.20 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 5 | 71.30 | 64.32 | 93.17 | 12.29 |
| db_read_all | 5 | 12.15 | 11.24 | 12.95 | 0.61 |
| db_read_random_100 | 5 | 349.58 | 305.36 | 432.44 | 50.45 |
| db_update_all | 5 | 27.29 | 22.85 | 32.52 | 3.83 |
| db_update_random_100 | 5 | 373.05 | 330.46 | 451.07 | 45.83 |
| db_delete_all | 5 | 43.32 | 39.00 | 49.03 | 3.71 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
