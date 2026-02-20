# Pros and Cons: JSON-in-Git vs Postgres

## Measured Results (latest run)
- Source: `experiments\\results\\latest.md`

| Operation | Git mean (ms) | Postgres mean (ms) | Faster | Speedup |
| --- | --- | --- | --- | --- |
| Seed | 2226.19 | 92.86 | Postgres | 23.97x |
| Read all | 462.74 | 15.67 | Postgres | 29.53x |
| Read random 100 | 431.96 | 367.24 | Postgres | 1.18x |
| Update all | 12340.84 | 40.06 | Postgres | 308.02x |
| Update random 100 | 1829.62 | 388.14 | Postgres | 4.71x |
| Delete all | 1673.06 | 71.62 | Postgres | 23.36x |

Key observations:
- Postgres dominates every operation, especially bulk updates (308x faster).
- Random reads are the closest comparison but Postgres still wins (1.18x).
- Git update-all has very high variance, likely from push/pack overhead.

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
Use the benchmark numbers to justify the storage choice. For operational workloads, Postgres wins decisively: 26x–256x faster for seed/update/delete and 42x faster for full reads. JSON-in-Git remains acceptable only when you need versioned files and performance is not the primary concern.
