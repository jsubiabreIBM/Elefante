# Dashboard Snapshot Contract (`dashboard_snapshot.json`)

This document defines the **required** and **optional** fields for the dashboard snapshot file consumed by the dashboard server.

## Location

- The dashboard server reads from: `DATA_DIR/dashboard_snapshot.json`
- In typical installs, `DATA_DIR` resolves to `~/.elefante/data`.

## Top-level schema

Required:

- `generated_at`: ISO-8601 timestamp (string)
- `nodes`: array of node objects
- `edges`: array of edge objects
- `stats`: object with basic counts

Recommended:

- `curation`: object capturing snapshot curation provenance

### `stats`

Required keys:

- `total_nodes`: integer
- `memories`: integer
- `entities`: integer
- `edges`: integer

## Node schema

Each element of `nodes` is an object:

Required:

- `id`: string (unique)
- `type`: string (typically `memory`, `signal`, `entity`)
- `name`: string (display label; for memories this should be curated)

Optional / recommended:

- `description`: string
- `created_at`: ISO-8601 timestamp string
- `properties`: object (free-form)

### Memory node expectations

For `type == "memory"`, `properties` should include:

- `content`: raw text (may be present but should not be shown by default in UI)
- `title`: curated title (string)
- `summary`: curated one-sentence summary (string)

Classification (recommended, V5):

- `ring`, `topic`, `knowledge_type`

## Edge schema

Each element of `edges` is an object:

Required:

- `from` or `source`: node id (string)
- `to` or `target`: node id (string)

Recommended:

- `type`: string (`signal`, `cohesion`, `graph`, `semantic`, etc.)
- `label`: string
- `similarity`: number (only for semantic)

## Invariants

- Every edge endpoint must reference an existing node id.
- Node ids are unique.
- `stats.*` should match actual counts (validator will check and warn).
