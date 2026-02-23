# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T08:57:04.298309+00:00
- Count: 1000
- Runs: 4
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T085528Z
- Git data dir: git_data
- Git remote: https://gitlab.com/grumlebob-group/grumlebob-project.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 3027.37 | 76.00 | Postgres | 39.83x |
| Read all | 1707.64 | 12.23 | Postgres | 139.66x |
| Read random 100 | 1604.62 | 362.01 | Postgres | 4.43x |
| Update all | 7924.27 | 28.84 | Postgres | 274.72x |
| Update random 100 | 3056.31 | 391.70 | Postgres | 7.80x |
| Delete all | 2673.98 | 45.26 | Postgres | 59.08x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 4 | 3027.37 | 2942.21 | 3088.43 | 61.45 |
| git_read_all | 4 | 1707.64 | 1560.01 | 2028.11 | 217.20 |
| git_read_random_100 | 4 | 1604.62 | 1544.41 | 1669.96 | 64.23 |
| git_update_all | 4 | 7924.27 | 7514.27 | 8097.84 | 276.48 |
| git_update_random_100 | 4 | 3056.31 | 2843.33 | 3553.34 | 333.12 |
| git_delete_all | 4 | 2673.98 | 2486.23 | 2811.03 | 148.43 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 4 | 76.00 | 72.52 | 81.29 | 3.74 |
| db_read_all | 4 | 12.23 | 11.75 | 12.67 | 0.43 |
| db_read_random_100 | 4 | 362.01 | 320.38 | 425.23 | 44.89 |
| db_update_all | 4 | 28.84 | 26.63 | 31.05 | 1.90 |
| db_update_random_100 | 4 | 391.70 | 349.87 | 499.66 | 72.16 |
| db_delete_all | 4 | 45.26 | 39.86 | 56.24 | 7.44 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
