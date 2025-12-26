# Changelog

All notable changes to Elefante will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] - Planned for v1.2.0

### Added
- Agent-managed enrichment architecture: Elefante never calls an LLM; agents pass enrichment via tool inputs.
- Auto-classification of domain/category via LLM
- Smart UPDATE (merge instead of duplicate)
- Automatic relationship inference
- Knowledge clustering

### Changed
- MCP tool names standardized with an `elefante*` prefix (see MCP tool list in `src/mcp/server.py`).
- Protocol injection key standardized to `MANDATORY_PROTOCOLS_READ_THIS_FIRST`.
- Dashboard semantic zoom
- Improved label rendering

### Removed
- Internal LLM connectivity and config/env overrides for LLM providers.
- OpenAI-based embeddings provider path (embeddings are local-only via sentence-transformers).

---

## [1.1.0] - 2025-12-26

### Summary

Transaction-scoped locking for true multi-IDE safety. Fixes the fundamental lock deadlock problem where stale locks from crashed/closed IDEs would block other instances indefinitely.

### The Problem Solved

v1.0.1 used **session-based locking**:
- `elefanteSystemEnable` acquired locks → held indefinitely
- `elefanteSystemDisable` released locks only on explicit call
- Crashed processes left stale locks forever (e.g., PID 4563 from Dec 14 blocking all access on Dec 26)
- Multiple IDEs could never interleave operations

### The Solution

v1.1.0 uses **transaction-scoped locking**:
- Each write operation acquires lock → does work → releases lock (milliseconds)
- Read operations are lock-free
- Stale locks auto-expire after 30 seconds
- Multiple IDEs can interleave operations safely

### Changes

#### Transaction-Scoped Locking (`src/utils/elefante_mode.py`)
- **NEW**: `TransactionLock` class - short-lived, auto-releasing locks
- **NEW**: `write_lock()` context manager for write operations
- **NEW**: `read_lock()` context manager (no-op - reads are lock-free)
- **NEW**: Stale lock detection (dead PID or timeout > 30s)
- **CHANGED**: `is_enabled` always returns `True` (no more enable/disable ceremony)
- **CHANGED**: `enable()`/`disable()` are now no-ops for backward compatibility
- **REMOVED**: Session-based lock files (`chroma.lock`, `kuzu.lock`)
- **ADDED**: Single `write.lock` file with PID/timestamp tracking

#### MCP Server Updates (`src/mcp/server.py`)
- **CHANGED**: Write operations wrapped in `write_lock()`:
  - `_handle_add_memory`
  - `_handle_create_entity`
  - `_handle_create_relationship`
  - `_handle_consolidate_memories`
  - `_handle_set_elefante_connection`
  - `_handle_etl_classify`
  - `_handle_migrate_memories_v3`
- **REMOVED**: Blocking mode check that returned "disabled" response
- **ADDED**: Graceful retry response when lock unavailable

### Migration

No migration needed. v1.1.0 is backward compatible:
- `elefanteSystemEnable` still works (now a no-op that returns success)
- `elefanteSystemDisable` still works (clears resources)
- All existing tool calls work unchanged

### Versioning Logic

Elefante follows [Semantic Versioning](https://semver.org/):
- **MAJOR** (x.0.0): Breaking changes requiring user action
- **MINOR** (1.x.0): New features, backward compatible
- **PATCH** (1.0.x): Bug fixes, documentation

This release is **1.1.0** (minor) because:
- New feature (transaction-scoped locking)
- Backward compatible (existing tools work unchanged)
- No user migration required

---

## [1.0.1] - 2025-12-11

### Summary

Critical update addressing protocol enforcement and multi-IDE safety.

### Changes

#### Auto-Inject Pitfalls (Protocol Enforcement)
- MCP Server now injects mandatory protocols (`MANDATORY_PROTOCOLS_READ_THIS_FIRST`) directly into every tool response
- Context-Aware Warnings for `addMemory` (integrity), `searchMemories` (bias), and graph tools (consistency)
- Updated `ai-behavior-compendium.md` with Issue #6 (Passive Protocol Enforcement Failure)

#### ELEFANTE_MODE (Multi-IDE Safety)
- **Problem**: Multiple IDEs accessing same databases caused crashes/lock conflicts
- **Solution**: Server starts OFF by default, user must explicitly enable

##### New MCP Tools
- `elefanteSystemEnable` - Acquires exclusive locks, enables memory operations
- `elefanteSystemDisable` - Releases locks, cleans up, returns to OFF state
- `elefanteSystemStatusGet` - Shows current mode, lock status, holder info (and stats when enabled)

##### New Files
- `src/utils/elefante_mode.py` - Lock management singleton
- `config.yaml` -> `elefante_mode:` section added

##### Behavior
- When **OFF**: Memory tools return graceful "disabled" response with instructions
- When **ON**: Full functionality with exclusive database access
- Lock files stored in `~/.elefante/locks/` with PID/timestamp tracking
- Safe tools (`elefanteSystemEnable`, `elefanteSystemDisable`, `elefanteSystemStatusGet`, `elefanteDashboardOpen`) always available

##### Usage
```
User: "Enable Elefante"
Agent calls: elefanteSystemEnable -> Acquires locks -> Memory tools now work

User: "Disable Elefante" (before switching IDEs)
Agent calls: elefanteSystemDisable -> Releases locks -> Safe for other IDE
```

---

## [1.0.0] - 2025-12-06

### Summary
First stable production release with comprehensive documentation cleanup.

### Core Features
- **Triple-Layer Memory Architecture**
  - ChromaDB for semantic/vector search
  - Kuzu for knowledge graph relationships
  - Session context for conversation continuity

- **MCP Server with 15 Tools**
  - `addMemory` - Store with intelligent ingestion (NEW/REDUNDANT/RELATED/CONTRADICTORY)
  - `searchMemories` - Hybrid search (semantic + structured + context)
  - `queryGraph` - Execute Cypher queries on knowledge graph
  - `getContext` - Retrieve comprehensive session context
  - `createEntity` - Create nodes in knowledge graph
  - `createRelationship` - Link entities with relationships
  - `getEpisodes` - Browse past sessions with summaries
  - `getSystemStatus` - Mode + lock info + (when enabled) system stats
  - `consolidateMemories` - Merge duplicates & resolve contradictions
  - `listAllMemories` - Export/inspect all memories
  - `getElefanteDashboard` - Launch visual Knowledge Garden UI (optionally refresh)
  - `setElefanteConnection` - Upsert entities + create relationships in one call
  - `migrateMemoriesV3` - Admin schema migration to V3

- **Cognitive Memory Model**
  - Agent-managed enrichment of emotions, intent, entities, relationships (no internal LLM calls)
  - Strategic insight generation
  - ADD/UPDATE/IGNORE action logic

- **Temporal Memory Decay**
  - Memories decay over time
  - Reinforced on access
  - Configurable decay rate

- **Visual Dashboard**
  - React/Vite frontend at http://127.0.0.1:8000
  - Force-directed graph visualization
  - Node inspector with full details

- **Automated Installation**
  - Pre-flight checks for common issues
  - Kuzu 0.11+ compatibility handling
  - IDE auto-configuration (VS Code, Cursor)

### Documentation
- Neural Register architecture (5 master registers)
- Domain compendiums for issue tracking
- Technical reference documentation
- Planning roadmaps

### Known Limitations
- Memory Schema V2 taxonomy (domain/category) requires manual input - auto-classification planned for v1.1.0
- Dashboard UX needs improvement - semantic zoom planned
- Smart UPDATE (merge) not yet implemented

---

## Pre-1.0 Development History

Development prior to v1.0.0 used inflated version numbers during rapid iteration.
These have been consolidated into this baseline release.

| Date | Internal Label | What Happened |
|------|----------------|---------------|
| 2025-11-27 | "v1.1.0" | Initial repository setup |
| 2025-12-02 | "v1.2.0" | User profile integration |
| 2025-12-04 | "v1.2.0" | Kuzu reserved word fix (`properties` -> `props`) |
| 2025-12-05 | "v1.3.0" | Documentation cleanup |
| 2025-12-06 | **v1.0.0** | Official baseline release |

---

## Migration Notes

### From Pre-1.0 Development
If upgrading from internal development versions:
1. Database schema changed (`properties` -> `props`)
2. Run `python scripts/init_databases.py` to reinitialize
3. Documentation restructured into `technical/`, `debug/`, `planning/`, `archive/`

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.