# Benchmark Results

## Run Info

- Run UTC: 2026-02-23T08:54:31.901701+00:00
- Count: 100
- Runs: 4
- Sample size: 100
- Table: DataLocations
- Git branch: main-base-20260223T085322Z
- Git data dir: git_data
- Git remote: https://gitlab.com/grumlebob-group/grumlebob-project.git

## Summary (Mean ms)

| Operation | Git (remote) | Postgres | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 2444.62 | 51.43 | Postgres | 47.53x |
| Read all | 1733.25 | 10.13 | Postgres | 171.12x |
| Read random 100 | 1608.19 | 409.25 | Postgres | 3.93x |
| Update all | 3165.83 | 18.63 | Postgres | 169.91x |
| Update random 100 | 3515.53 | 345.80 | Postgres | 10.17x |
| Delete all | 2398.33 | 42.76 | Postgres | 56.09x |

## Git Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| git_seed | 4 | 2444.62 | 2270.51 | 2613.65 | 159.19 |
| git_read_all | 4 | 1733.25 | 1512.86 | 2005.78 | 207.73 |
| git_read_random_100 | 4 | 1608.19 | 1554.55 | 1709.56 | 69.06 |
| git_update_all | 4 | 3165.83 | 2919.20 | 3339.13 | 190.18 |
| git_update_random_100 | 4 | 3515.53 | 2929.90 | 4878.59 | 924.03 |
| git_delete_all | 4 | 2398.33 | 2317.06 | 2523.93 | 99.16 |

## Postgres Benchmarks

| Benchmark | Runs | Mean (ms) | Min (ms) | Max (ms) | Stdev (ms) |
| --- | --- | --- | --- | --- | --- |
| db_seed | 4 | 51.43 | 44.38 | 66.36 | 10.07 |
| db_read_all | 4 | 10.13 | 9.37 | 11.32 | 0.92 |
| db_read_random_100 | 4 | 409.25 | 337.33 | 534.95 | 89.87 |
| db_update_all | 4 | 18.63 | 17.53 | 20.64 | 1.38 |
| db_update_random_100 | 4 | 345.80 | 333.94 | 362.03 | 12.98 |
| db_delete_all | 4 | 42.76 | 38.51 | 47.92 | 4.64 |


## Notes
- Git benchmarks fetch from a remote repo and read committed blobs (no working tree reads).
- Seed benchmarks use new orphan branches each run; other Git tests use a pre-seeded base commit.
- Connection setup is excluded; DB connection stays open during benchmarks.
- Speedup is the ratio of slower to faster (higher means bigger gap).
