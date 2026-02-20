# Benchmark Results

## Run Info

- Run UTC: 2026-02-20T09:11:23.174914+00:00
- Count: 1500
- Runs: 20
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260220T090419Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 2226.19 | 92.86 | Postgres | 23.97x |
| Read all | 462.74 | 15.67 | Postgres | 29.53x |
| Read random 100 | 431.96 | 367.24 | Postgres | 1.18x |
| Update all | 12340.84 | 40.06 | Postgres | 308.02x |
| Update random 100 | 1829.62 | 388.14 | Postgres | 4.71x |
| Delete all | 1673.06 | 71.62 | Postgres | 23.36x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 20 | 2226.19 | 2109.59 | 2352.17 | 74.55 |
| git_read_all | 20 | 462.74 | 403.77 | 769.15 | 88.92 |
| git_read_random_100 | 20 | 431.96 | 396.35 | 530.82 | 43.75 |
| git_update_all | 20 | 12340.84 | 9123.35 | 34723.46 | 7544.27 |
| git_update_random_100 | 20 | 1829.62 | 1734.31 | 2177.32 | 87.11 |
| git_delete_all | 20 | 1673.06 | 1394.40 | 1818.06 | 79.82 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 20 | 92.86 | 74.18 | 155.07 | 20.69 |
| db_read_all | 20 | 15.67 | 12.26 | 18.02 | 1.40 |
| db_read_random_100 | 20 | 367.24 | 317.46 | 443.98 | 40.84 |
| db_update_all | 20 | 40.06 | 31.08 | 79.02 | 9.64 |
| db_update_random_100 | 20 | 388.14 | 340.13 | 493.76 | 32.46 |
| db_delete_all | 20 | 71.62 | 54.47 | 86.49 | 7.25 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
