# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T09:15:25.213093+00:00
- Count: 15000
- Runs: 4
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T090557Z
- Git data dir: git_data
- Git remote: https://gitlab.com/grumlebob-group/grumlebob-project.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 7695.88 | 387.01 | Postgres | 19.89x |
| Read all | 1952.94 | 38.80 | Postgres | 50.34x |
| Read random 100 | 1628.25 | 330.57 | Postgres | 4.93x |
| Update all | 93976.25 | 169.94 | Postgres | 553.01x |
| Update random 100 | 4711.60 | 360.71 | Postgres | 13.06x |
| Delete all | 6144.49 | 64.44 | Postgres | 95.36x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 4 | 7695.88 | 7530.33 | 7967.81 | 197.49 |
| git_read_all | 4 | 1952.94 | 1704.13 | 2313.77 | 284.93 |
| git_read_random_100 | 4 | 1628.25 | 1570.36 | 1672.87 | 47.81 |
| git_update_all | 4 | 93976.25 | 85604.63 | 117375.29 | 15608.84 |
| git_update_random_100 | 4 | 4711.60 | 3581.72 | 7951.85 | 2160.49 |
| git_delete_all | 4 | 6144.49 | 4515.67 | 6779.50 | 1087.84 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 4 | 387.01 | 273.53 | 574.98 | 132.70 |
| db_read_all | 4 | 38.80 | 34.22 | 44.92 | 4.54 |
| db_read_random_100 | 4 | 330.57 | 317.26 | 338.49 | 9.42 |
| db_update_all | 4 | 169.94 | 160.66 | 180.63 | 8.44 |
| db_update_random_100 | 4 | 360.71 | 326.26 | 377.95 | 23.33 |
| db_delete_all | 4 | 64.44 | 57.83 | 71.29 | 5.91 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
