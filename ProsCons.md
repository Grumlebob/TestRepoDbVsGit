# Pros and Cons: JSON-in-Git vs Postgres

## Measured Results (parameter sweep)

- Sources:
  - `experiments\\results\\n100_github\\latest.md`
  - `experiments\\results\\n100_gitlab\\latest.md`
  - `experiments\\results\\n1000_github\\latest.md`
  - `experiments\\results\\n1000_gitlab\\latest.md`
  - `experiments\\results\\n15000_github\\latest.md`
  - `experiments\\results\\n15000_gitlab\\latest.md`

### N=100 (runs=4)

GitHub:

| Operation         | Git mean (ms) | Postgres mean (ms) | Faster   | Speedup |
| ----------------- | ------------- | ------------------ | -------- | ------- |
| Seed              | 1210.91       | 56.59              | Postgres | 21.40x  |
| Read all          | 481.64        | 11.33              | Postgres | 42.52x  |
| Read random 100   | 411.86        | 392.64             | Postgres | 1.05x   |
| Update all        | 1793.83       | 20.95              | Postgres | 85.60x  |
| Update random 100 | 1813.75       | 349.82             | Postgres | 5.18x   |
| Delete all        | 1255.81       | 38.99              | Postgres | 32.21x  |

GitLab:

| Operation         | Git mean (ms) | Postgres mean (ms) | Faster   | Speedup |
| ----------------- | ------------- | ------------------ | -------- | ------- |
| Seed              | 2444.62       | 51.43              | Postgres | 47.53x  |
| Read all          | 1733.25       | 10.13              | Postgres | 171.12x |
| Read random 100   | 1608.19       | 409.25             | Postgres | 3.93x   |
| Update all        | 3165.83       | 18.63              | Postgres | 169.91x |
| Update random 100 | 3515.53       | 345.80             | Postgres | 10.17x  |
| Delete all        | 2398.33       | 42.76              | Postgres | 56.09x  |

### N=1000 (runs=4)

GitHub:

| Operation         | Git mean (ms) | Postgres mean (ms) | Faster   | Speedup |
| ----------------- | ------------- | ------------------ | -------- | ------- |
| Seed              | 1883.04       | 79.51              | Postgres | 23.68x  |
| Read all          | 497.19        | 15.45              | Postgres | 32.17x  |
| Read random 100   | 432.37        | 369.16             | Postgres | 1.17x   |
| Update all        | 6831.21       | 28.60              | Postgres | 238.86x |
| Update random 100 | 1945.25       | 372.83             | Postgres | 5.22x   |
| Delete all        | 1633.99       | 43.56              | Postgres | 37.51x  |

GitLab:

| Operation         | Git mean (ms) | Postgres mean (ms) | Faster   | Speedup |
| ----------------- | ------------- | ------------------ | -------- | ------- |
| Seed              | 3027.37       | 76.00              | Postgres | 39.83x  |
| Read all          | 1707.64       | 12.23              | Postgres | 139.66x |
| Read random 100   | 1604.62       | 362.01             | Postgres | 4.43x   |
| Update all        | 7924.27       | 28.84              | Postgres | 274.72x |
| Update random 100 | 3056.31       | 391.70             | Postgres | 7.80x   |
| Delete all        | 2673.98       | 45.26              | Postgres | 59.08x  |

### N=15000 (runs=4)

GitHub:

| Operation         | Git mean (ms) | Postgres mean (ms) | Faster   | Speedup |
| ----------------- | ------------- | ------------------ | -------- | ------- |
| Seed              | 5662.49       | 335.16             | Postgres | 16.89x  |
| Read all          | 604.47        | 37.66              | Postgres | 16.05x  |
| Read random 100   | 512.67        | 327.29             | Postgres | 1.57x   |
| Update all        | 85632.81      | 175.45             | Postgres | 488.08x |
| Update random 100 | 3353.57       | 351.97             | Postgres | 9.53x   |
| Delete all        | 4722.64       | 45.63              | Postgres | 103.49x |

GitLab:

| Operation         | Git mean (ms) | Postgres mean (ms) | Faster   | Speedup |
| ----------------- | ------------- | ------------------ | -------- | ------- |
| Seed              | 7695.88       | 387.01             | Postgres | 19.89x  |
| Read all          | 1952.94       | 38.80              | Postgres | 50.34x  |
| Read random 100   | 1628.25       | 330.57             | Postgres | 4.93x   |
| Update all        | 93976.25      | 169.94             | Postgres | 553.01x |
| Update random 100 | 4711.60       | 360.71             | Postgres | 13.06x  |
| Delete all        | 6144.49       | 64.44              | Postgres | 95.36x  |

### Side-by-side summary (GitHub vs GitLab)

| N     | Operation         | GitHub Git (ms) | GitHub DB (ms) | GitHub Speedup | GitLab Git (ms) | GitLab DB (ms) | GitLab Speedup |
| ----- | ----------------- | -------------- | -------------- | -------------- | --------------- | -------------- | -------------- |
| 100   | Seed              | 1210.91        | 56.59          | 21.40x         | 2444.62         | 51.43          | 47.53x         |
| 100   | Read all          | 481.64         | 11.33          | 42.52x         | 1733.25         | 10.13          | 171.12x        |
| 100   | Read random 100   | 411.86         | 392.64         | 1.05x          | 1608.19         | 409.25         | 3.93x          |
| 100   | Update all        | 1793.83        | 20.95          | 85.60x         | 3165.83         | 18.63          | 169.91x        |
| 100   | Update random 100 | 1813.75        | 349.82         | 5.18x          | 3515.53         | 345.80         | 10.17x         |
| 100   | Delete all        | 1255.81        | 38.99          | 32.21x         | 2398.33         | 42.76          | 56.09x         |
| 1000  | Seed              | 1883.04        | 79.51          | 23.68x         | 3027.37         | 76.00          | 39.83x         |
| 1000  | Read all          | 497.19         | 15.45          | 32.17x         | 1707.64         | 12.23          | 139.66x        |
| 1000  | Read random 100   | 432.37         | 369.16         | 1.17x          | 1604.62         | 362.01         | 4.43x          |
| 1000  | Update all        | 6831.21        | 28.60          | 238.86x        | 7924.27         | 28.84          | 274.72x        |
| 1000  | Update random 100 | 1945.25        | 372.83         | 5.22x          | 3056.31         | 391.70         | 7.80x          |
| 1000  | Delete all        | 1633.99        | 43.56          | 37.51x         | 2673.98         | 45.26          | 59.08x         |
| 15000 | Seed              | 5662.49        | 335.16         | 16.89x         | 7695.88         | 387.01         | 19.89x         |
| 15000 | Read all          | 604.47         | 37.66          | 16.05x         | 1952.94         | 38.80          | 50.34x         |
| 15000 | Read random 100   | 512.67         | 327.29         | 1.57x          | 1628.25         | 330.57         | 4.93x          |
| 15000 | Update all        | 85632.81       | 175.45         | 488.08x        | 93976.25        | 169.94         | 553.01x        |
| 15000 | Update random 100 | 3353.57        | 351.97         | 9.53x          | 4711.60         | 360.71         | 13.06x         |
| 15000 | Delete all        | 4722.64        | 45.63          | 103.49x        | 6144.49         | 64.44          | 95.36x         |

### Super-clean summary (speedup by N)

Speedup order: N=100 / 1000 / 15000.

| Operation         | GitHub speedup | GitLab speedup |
| ----------------- | -------------- | -------------- |
| Seed              | 21.40x / 23.68x / 16.89x | 47.53x / 39.83x / 19.89x |
| Read all          | 42.52x / 32.17x / 16.05x | 171.12x / 139.66x / 50.34x |
| Read random 100   | 1.05x / 1.17x / 1.57x | 3.93x / 4.43x / 4.93x |
| Update all        | 85.60x / 238.86x / 488.08x | 169.91x / 274.72x / 553.01x |
| Update random 100 | 5.18x / 5.22x / 9.53x | 10.17x / 7.80x / 13.06x |
| Delete all        | 32.21x / 37.51x / 103.49x | 56.09x / 59.08x / 95.36x |

Key observations:

- Postgres dominates all operations for both GitHub and GitLab remotes; the gap widens dramatically for update-all as N grows.
- GitLab remote Git operations are consistently slower than GitHub, while Postgres timings stay in the same range.
- Random reads are the closest comparison; GitHub is ~1.05x to ~1.57x slower, GitLab is ~3.9x to ~4.9x slower.
- Git update-all and delete-all scale poorly due to commit + push overhead; update-all reaches ~85s (GitHub) and ~94s (GitLab) at N=15000.

----Egne pros/Cons for git vs db----
DB naturally supports Authorization.

Den kan ikke modelere dependencies

DB tools have plenty of common operations, like CRUD, etc. Also things like creating indexes, for what is being looked up. Git DOESN'T. It wants manual handling of files and then commiting changes.

Also DataLocations are often composite, based on Experiment and Inputbox - Git doesn't support composite keys naturally. This makes it more easy to reuse datalocations, like having a different experiment and inputbox point to same data location without storing it twice.

DB have stored procedures and triggers, and in general consumer producer patterns, with ACID properties.
Git have github actions.

Git = Utrolig visible. Inbygget UI. Query med clicks. DB kræver næsten en lille SQL forståelse eller egne byggede tools.

Git = Skal have beskeder.
DB = Mere silent, fordi det blot er row operationer.

## JSON Files in Git (Remote)

Pros:

- Simple to inspect and edit with any text editor.
- Built-in history, diffs, and audit trail via Git.
- Easy to backup and move as a folder.
- No database server required.

Cons:

- Bulk operations are slow: commit + push dominates.
- Repo bloat and slow Git operations with many large files.
- Hard to enforce schema or data integrity.
- Merge conflicts are common for concurrent edits.
- File system metadata overhead grows with file count.

## Postgres Table (`DataLocations`)

Pros:

- Fast bulk reads/updates with a single query.
- Strong consistency and transactional safety.
- Rich querying, indexing, and filtering.
- Scales to large datasets without repo growth.

Cons:

- Requires running a database server and credentials.
- Slightly more setup and operational overhead.
- Data is not directly human-diffable in Git.
- Need migrations or schema management over time.
- Connection latency can dominate small, many-query workloads.

## Practical Takeaways

- If you keep random access in the DB, batch the ids (`WHERE id IN (...)`) to reduce per-query latency.
- If you must use JSON-in-Git, consider chunking multiple records per file to reduce file count.
- For Git remote reads, prefer fetching once and reading locally when possible.
- Use Postgres for operational workloads; use Git for versioned configuration or small, rarely-changed datasets.

## Conclusion

Use the benchmark numbers to justify the storage choice. For operational workloads, Postgres wins decisively: across N=100..15000 and both remotes, seed/update/delete are roughly 16.9x–553x faster, full reads are about 16.0x–171x faster, and random reads are about 1.05x–4.93x faster. JSON-in-Git remains acceptable only when you need versioned files and performance is not the primary concern.
