# Scripts naming convention

Goal: make each script name immediately communicate **purpose** and **scope**.

## Pattern

- `verb_object[_qualifier].py` (snake_case)
- Use clear verbs: `install`, `configure`, `verify`, `export`, `ingest`, `migrate`, `update`, `inspect`, `demo`, `debug`.
- Put experimental/one-off helpers under `scripts/debug/` or name them with a `debug_` prefix.

## Examples in this repo

- `configure_*` = write IDE/MCP client configs
- `verify_*` = run checks (health, protocol handshakes, repo hygiene)
- `export_*` / `ingest_*` / `migrate_*` = data workflows
- `disable_elefante_mode.py` = turn off Elefante Mode + show lock status

If you need a new script, prefer adding a new `verb_object` script rather than creating another near-duplicate with a vague name.
