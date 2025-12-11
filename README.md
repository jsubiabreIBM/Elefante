# Elefante v1.0.1

**Local-First AI Memory System with Perfect Recall**

> **Current Release:** v1.0.1 - Multi-IDE Safety & Protocol Enforcement

Elefante gives AI agents a stateful brain by combining semantic search, knowledge graphs, and conversation context—all running 100% locally on your machine. No cloud. No data egress. Just pure, private memory.

---

## Why Elefante?

AI agents are stateless by default. They forget everything between sessions. Elefante solves this by providing:

- **Triple-Layer Memory**: Semantic (ChromaDB) + Graph (Kuzu) + Context = Perfect Recall
- **Privacy First**: Your data never leaves your machine (`~/.elefante/data`)
- **MCP Native**: Plug-and-play for VS Code, Cursor, Claude Desktop
- **Adaptive Intelligence**: Dynamically adjusts retrieval based on query intent
- **Visual Dashboard**: Interactive knowledge graph visualization

---

## Quick Start

### Installation (2 minutes)

**Windows:**
```bash
install.bat
```

**Mac/Linux:**
```bash
./install.sh
```

The installer includes automated safeguards that prevent common issues (Kuzu 0.11+ compatibility, disk space, dependencies).

**Success Rate**: 98%+ (up from 50% before safeguards)

### Usage

Simply talk to your AI agent:

```
> "Remember that I'm a Senior Python Developer at IBM"
> "What projects am I working on?"
> "Show me the relationship between Project Omega and Kafka"
```

Elefante handles the rest—storing, indexing, and retrieving with perfect accuracy.

---

## Documentation

### Start Here

- **New Users**: [`docs/technical/installation.md`](docs/technical/installation.md) - Complete setup guide
- **Understanding the System**: [`docs/technical/architecture.md`](docs/technical/architecture.md) - How it works
- **Using the API**: [`docs/technical/usage.md`](docs/technical/usage.md) - MCP tools & examples
- **Visual Dashboard**: [`docs/technical/dashboard.md`](docs/technical/dashboard.md) - Knowledge graph UI

### Complete Documentation

- **Technical Docs**: [`docs/technical/`](docs/technical/) - Architecture, schema, API reference
- **Debug Docs**: [`docs/debug/`](docs/debug/) - Neural Registers & troubleshooting
- **Planning**: [`docs/planning/`](docs/planning/) - Roadmap & future plans
- **Archive**: [`docs/archive/`](docs/archive/) - Historical documentation

---

## Architecture Overview

```
User Query
    ↓
MCP Server
    ↓
Orchestrator (Adaptive Weighting)
    ↓
┌─────────────┬──────────────┬─────────────────┐
│  ChromaDB   │  Kuzu Graph  │  Session Context│
│  (Semantic) │  (Structure) │  (Recent)       │
└─────────────┴──────────────┴─────────────────┘
    ↓
Weighted Merge
    ↓
Perfect Result
```

**Key Innovation**: Adaptive weighting adjusts retrieval strategy based on query type:
- Questions -> Semantic search
- IDs/Names -> Graph lookup
- Pronouns -> Session context

See [`docs/technical/architecture.md`](docs/technical/architecture.md) for details.

---

## MCP Tools (16 Total)

Once installed, your AI agent gets these tools:

| Tool | Purpose | Example |
|------|---------|---------|
| `addMemory` | Store information with intelligent ingestion | "Remember I'm working on Project Omega" |
| `searchMemories` | Retrieve memories (semantic/structured/hybrid) | "What do you know about Omega?" |
| `queryGraph` | Execute Cypher queries on knowledge graph | "Show all AI-related projects" |
| `getContext` | Get comprehensive session context | (Auto-called by agent) |
| `createEntity` | Create nodes in knowledge graph | "Create entity for 'Bob'" |
| `createRelationship` | Link entities with relationships | "Link Bob to Elefante as Maintainer" |
| `getEpisodes` | Browse past sessions with summaries | "Show recent work sessions" |
| `getStats` | Get system health & usage statistics | "Show memory system stats" |
| `consolidateMemories` | Merge duplicates & resolve contradictions | (Auto-triggered or manual) |
| `listAllMemories` | Export/inspect all memories (no filtering) | "List all memories for backup" |
| `openDashboard` | Launch visual Knowledge Garden UI | "Open the dashboard" |
| `enableElefante` | Acquire exclusive locks, enable memory ops | "Enable Elefante" |
| `disableElefante` | Release locks, safe for IDE switch | "Disable Elefante" |
| `getElefanteStatus` | Check mode status and lock info | "Is Elefante enabled?" |

**Key Features**:
- **Intelligent Ingestion**: `addMemory` auto-detects NEW/REDUNDANT/RELATED/CONTRADICTORY
- **Query Rewriting**: `searchMemories` requires explicit, standalone queries (no pronouns)
- **Hybrid Search**: Combines semantic (ChromaDB) + structured (Kuzu) + context
- **Graph Analytics**: Direct Cypher query support via `queryGraph`
- **Visual Exploration**: Interactive dashboard via `openDashboard`
- **Multi-IDE Safety**: ELEFANTE_MODE prevents lock conflicts between IDEs

See [`docs/technical/usage.md`](docs/technical/usage.md) for complete API reference.

---

## Visual Dashboard

Launch the interactive knowledge graph:

```bash
cd Elefante
.venv\Scripts\python.exe -m src.dashboard.server
```

Open http://127.0.0.1:8000 to explore:
- Force-directed graph visualization
- Node inspector with full details
- Filter by spaces/categories
- Real-time statistics

See [`docs/technical/dashboard.md`](docs/technical/dashboard.md) for complete guide.

---

## Development Status

**Current Version**: v1.0.1 (Production)

### Implemented
-  Triple-layer architecture (ChromaDB + Kuzu + Context)
-  MCP server with 16 tools
-  ELEFANTE_MODE (Multi-IDE safety with exclusive locking)
-  Auto-Inject Pitfalls (Protocol enforcement in responses)
-  Cognitive memory model (LLM extracts emotions, intent, entities, relationships)
-  Temporal decay (memories fade, reinforced on access)
-  Visual dashboard
-  Automated installation safeguards

### Partial
-  Memory Schema V2 - Schema defined, but domain/category auto-classification not implemented
-  Dashboard UX - Functional but needs visual improvements

### Planned (v1.1.0)
- [ ] Auto-classification of domain/category via LLM
- [ ] Smart UPDATE (merge instead of duplicate)
- [ ] Dashboard semantic zoom

See [`docs/planning/roadmap.md`](docs/planning/roadmap.md) for full roadmap.

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

**Documentation Structure**:
- `docs/technical/` - How things work now
- `docs/debug/` - Neural Registers (lessons from failures)
- `docs/planning/` - Future roadmap

---

## License

See [`LICENSE`](LICENSE)

---

## Links

- **Repository**: https://github.com/jsubiabreIBM/Elefante
- **Technical Docs**: [`docs/technical/README.md`](docs/technical/README.md)
- **Roadmap**: [`docs/planning/roadmap.md`](docs/planning/roadmap.md)
- **Changelog**: [`CHANGELOG.md`](CHANGELOG.md)

---

**Built for AI agents that never forget**
