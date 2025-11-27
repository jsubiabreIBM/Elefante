# 📁 Elefante Project Structure

This document describes the organization of the Elefante codebase (V1.0).

## Root Directory

```
Elefante/
├── install.bat          # Windows One-Click Installer
├── install.sh           # Mac/Linux One-Click Installer
├── config.yaml          # System Configuration
├── requirements.txt     # Python Dependencies
├── README.md            # Main Documentation
└── .env                 # Environment Variables (Optional)
```

## Source Code (`src/`)

### Core Modules (`src/core/`)

The brain of the system.

- `orchestrator.py` - **Main Entry Point**. Routes queries to Vector/Graph stores.
- `vector_store.py` - **ChromaDB** wrapper for semantic search.
- `graph_store.py` - **Kuzu** wrapper for structured knowledge.
- `conversation_context.py` - Handles short-term memory and session context.
- `scoring.py` - Adaptive weighting logic.
- `deduplication.py` - Merges duplicate results.

### Data Models (`src/models/`)

Pydantic definitions for type safety.

- `memory.py` - `Memory`, `MemoryType`, `MemoryMetadata`.
- `entity.py` - `Entity`, `Relationship`.
- `query.py` - `SearchResult`, `QueryPlan`.

### MCP Server (`src/mcp/`)

Integration with IDEs.

- `server.py` - Implements the Model Context Protocol.

### Utilities (`src/utils/`)

- `config.py` - Handles absolute paths and configuration loading.
- `logger.py` - Structured JSON logging.

## Scripts (`scripts/`)

System management utilities.

- `install.py` - **Core Installer Logic**. Used by `install.bat/sh`.
- `configure_vscode_bob.py` - Auto-configures IDE settings.
- `init_databases.py` - Creates/Resets database files.
- `health_check.py` - Verifies system status.
- `test_end_to_end.py` - Runs full system integration tests.

## Documentation (`docs/`)

- `SETUP.md` - Manual installation guide.
- `IDE_SETUP.md` - IDE integration guide.
- `TUTORIAL.md` - Usage examples.
- `ARCHITECTURE.md` - High-level design.
- `ARCHITECTURE_DEEP_DIVE.md` - Technical details.

## Data Directories (Auto-Generated)

These are created at runtime and **not** committed to Git.

- `data/chroma/` - Vector database files.
- `data/kuzu/` - Graph database files.
- `logs/` - System logs.
- `.venv/` - Python virtual environment.
