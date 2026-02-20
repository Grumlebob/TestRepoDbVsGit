# Benchmark Results

## Run Info

- Run UTC: 2026-02-20T09:15:36.183878+00:00
- Count: 100
- Runs: 10
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260220T091409Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 1229.85 | 52.52 | Postgres | 23.42x |
| Read all | 421.06 | 11.98 | Postgres | 35.15x |
| Read random 100 | 447.75 | 371.30 | Postgres | 1.21x |
| Update all | 1797.30 | 21.05 | Postgres | 85.40x |
| Update random 100 | 1874.49 | 392.49 | Postgres | 4.78x |
| Delete all | 1282.00 | 46.27 | Postgres | 27.71x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 10 | 1229.85 | 1160.59 | 1330.23 | 42.45 |
| git_read_all | 10 | 421.06 | 392.74 | 561.40 | 50.20 |
| git_read_random_100 | 10 | 447.75 | 411.99 | 531.23 | 47.30 |
| git_update_all | 10 | 1797.30 | 1747.74 | 1859.11 | 34.05 |
| git_update_random_100 | 10 | 1874.49 | 1799.00 | 2297.14 | 149.94 |
| git_delete_all | 10 | 1282.00 | 1256.63 | 1363.62 | 34.21 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 10 | 52.52 | 46.65 | 70.61 | 6.83 |
| db_read_all | 10 | 11.98 | 10.02 | 14.56 | 1.31 |
| db_read_random_100 | 10 | 371.30 | 346.58 | 439.27 | 26.91 |
| db_update_all | 10 | 21.05 | 18.03 | 25.78 | 2.68 |
| db_update_random_100 | 10 | 392.49 | 348.46 | 479.55 | 46.35 |
| db_delete_all | 10 | 46.27 | 37.83 | 56.53 | 5.57 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
