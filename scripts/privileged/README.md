# Privileged tools

These scripts are allowed to be dangerous.

Rules:
- Default must be safe (dry-run).
- Must require explicit authorization before destructive writes.
- Must take backups before deletion.

## memory_surgeon.py

Surgical memory removal with impact analysis.

Impact signals:
- Temporal relevance score (`Memory.calculate_relevance_score()`)
- Graph connectivity (degree + neighbors) when Kuzu is available
- Semantic connectivity (nearest-neighbor similarity using stored embeddings; no external embedding call)

Notes:
- If Kuzu is locked/unavailable, graph connectivity is marked unknown and deletion is refused in `--apply` mode.

Safety gates for deletion:
- `ELEFANTE_PRIVILEGED=1`
- `--apply`
- `--confirm DELETE`

Examples:
- Dry-run: `python scripts/privileged/memory_surgeon.py --auto test`
- Apply: `ELEFANTE_PRIVILEGED=1 python scripts/privileged/memory_surgeon.py --auto test --apply --confirm DELETE`

Backups:
- Writes a JSON backup under `~/.elefante/data/backups/memory_surgeon/` by default.
