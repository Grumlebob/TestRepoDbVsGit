# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T08:11:03.601206+00:00
- Count: 1000
- Runs: 5
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T080904Z
- Git data dir: git_data
- Git remote: https://gitlab.com/grumlebob-group/grumlebob-project.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 3025.29 | 87.82 | Postgres | 34.45x |
| Read all | 1713.79 | 12.90 | Postgres | 132.87x |
| Read random 100 | 1657.51 | 345.43 | Postgres | 4.80x |
| Update all | 8082.96 | 37.08 | Postgres | 217.96x |
| Update random 100 | 3133.04 | 378.13 | Postgres | 8.29x |
| Delete all | 2712.52 | 48.52 | Postgres | 55.90x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 5 | 3025.29 | 2806.74 | 3234.22 | 194.52 |
| git_read_all | 5 | 1713.79 | 1558.43 | 1926.73 | 138.41 |
| git_read_random_100 | 5 | 1657.51 | 1527.44 | 2010.19 | 198.94 |
| git_update_all | 5 | 8082.96 | 7786.94 | 8402.11 | 233.66 |
| git_update_random_100 | 5 | 3133.04 | 2898.38 | 3346.48 | 198.76 |
| git_delete_all | 5 | 2712.52 | 2456.98 | 2946.75 | 185.97 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 5 | 87.82 | 66.94 | 140.15 | 29.93 |
| db_read_all | 5 | 12.90 | 11.36 | 15.14 | 1.43 |
| db_read_random_100 | 5 | 345.43 | 335.81 | 360.03 | 9.09 |
| db_update_all | 5 | 37.08 | 28.61 | 55.31 | 10.91 |
| db_update_random_100 | 5 | 378.13 | 347.65 | 459.02 | 46.78 |
| db_delete_all | 5 | 48.52 | 41.14 | 53.59 | 4.73 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
