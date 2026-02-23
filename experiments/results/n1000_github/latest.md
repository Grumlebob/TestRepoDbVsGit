# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T08:42:09.069297+00:00
- Count: 1000
- Runs: 4
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T084103Z
- Git data dir: git_data
- Git remote: https://github.com/Grumlebob/TestRepoDbVsGit.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 1883.04 | 79.51 | Postgres | 23.68x |
| Read all | 497.19 | 15.45 | Postgres | 32.17x |
| Read random 100 | 432.37 | 369.16 | Postgres | 1.17x |
| Update all | 6831.21 | 28.60 | Postgres | 238.86x |
| Update random 100 | 1945.25 | 372.83 | Postgres | 5.22x |
| Delete all | 1633.99 | 43.56 | Postgres | 37.51x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 4 | 1883.04 | 1830.05 | 1970.69 | 60.90 |
| git_read_all | 4 | 497.19 | 411.19 | 629.03 | 99.18 |
| git_read_random_100 | 4 | 432.37 | 404.55 | 510.22 | 51.94 |
| git_update_all | 4 | 6831.21 | 6661.05 | 6928.85 | 120.19 |
| git_update_random_100 | 4 | 1945.25 | 1809.67 | 2213.36 | 181.74 |
| git_delete_all | 4 | 1633.99 | 1413.32 | 1743.58 | 154.91 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 4 | 79.51 | 70.91 | 97.35 | 12.35 |
| db_read_all | 4 | 15.45 | 12.29 | 21.52 | 4.12 |
| db_read_random_100 | 4 | 369.16 | 328.40 | 476.42 | 71.60 |
| db_update_all | 4 | 28.60 | 25.71 | 30.33 | 2.01 |
| db_update_random_100 | 4 | 372.83 | 343.39 | 400.58 | 24.49 |
| db_delete_all | 4 | 43.56 | 38.48 | 52.02 | 5.91 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
