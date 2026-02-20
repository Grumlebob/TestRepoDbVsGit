# Pros and Cons: JSON-in-Git vs Postgres

## Measured Results (parameter sweep)

- Sources:
  - `experiments\\results\\n100\\latest.md`
  - `experiments\\results\\n1000\\latest.md`
  - `experiments\\results\\n15000\\latest.md`

### N=100 (runs=10)

| Operation         | Git mean (ms) | Postgres mean (ms) | Faster   | Speedup |
| ----------------- | ------------- | ------------------ | -------- | ------- |
| Seed              | 1229.85       | 52.52              | Postgres | 23.42x  |
| Read all          | 421.06        | 11.98              | Postgres | 35.15x  |
| Read random 100   | 447.75        | 371.30             | Postgres | 1.21x   |
| Update all        | 1797.30       | 21.05              | Postgres | 85.40x  |
| Update random 100 | 1874.49       | 392.49             | Postgres | 4.78x   |
| Delete all        | 1282.00       | 46.27              | Postgres | 27.71x  |

### N=1000 (runs=10)

| Operation         | Git mean (ms) | Postgres mean (ms) | Faster   | Speedup |
| ----------------- | ------------- | ------------------ | -------- | ------- |
| Seed              | 1885.90       | 77.55              | Postgres | 24.32x  |
| Read all          | 478.07        | 15.90              | Postgres | 30.07x  |
| Read random 100   | 430.08        | 363.30             | Postgres | 1.18x   |
| Update all        | 12018.49      | 30.51              | Postgres | 393.87x |
| Update random 100 | 2080.91       | 395.45             | Postgres | 5.26x   |
| Delete all        | 1536.07       | 52.76              | Postgres | 29.11x  |

### N=15000 (runs=3)

| Operation         | Git mean (ms) | Postgres mean (ms) | Faster   | Speedup |
| ----------------- | ------------- | ------------------ | -------- | ------- |
| Seed              | 5697.33       | 342.00             | Postgres | 16.66x  |
| Read all          | 720.06        | 42.51              | Postgres | 16.94x  |
| Read random 100   | 421.52        | 348.95             | Postgres | 1.21x   |
| Update all        | 99237.96      | 234.42             | Postgres | 423.34x |
| Update random 100 | 3654.75       | 388.69             | Postgres | 9.40x   |
| Delete all        | 4547.86       | 54.20              | Postgres | 83.90x  |

Key observations:

- Postgres dominates all operations at every N; the gap widens dramatically for update-all as N grows.
- Random reads are the closest comparison; Postgres still wins but only by ~1.2x.
- Git update-all and delete-all scale poorly due to commit + push overhead.

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

Use the benchmark numbers to justify the storage choice. For operational workloads, Postgres wins decisively: across N=100..15000, seed/update/delete are roughly 16x–423x faster and full reads are about 17x–35x faster. JSON-in-Git remains acceptable only when you need versioned files and performance is not the primary concern.
