# Elefante Documentation

**Complete documentation index for Elefante AI Memory System v1.1.0**

---

## 🚀 Quick Navigation

| I want to... | Go to... |
|--------------|----------|
| Install Elefante | [`technical/installation.md`](technical/installation.md) |
| Understand the system | [`technical/architecture.md`](technical/architecture.md) |
| Use the MCP tools | [`technical/usage.md`](technical/usage.md) |
| Open the dashboard | [`technical/dashboard.md`](technical/dashboard.md) |
| Troubleshoot issues | [`debug/installation/never-again-guide.md`](debug/installation/never-again-guide.md) |
| See what's next | [`../NEXT_STEPS.md`](../NEXT_STEPS.md) |

---

## 📚 Documentation Structure

### [`technical/`](technical/) - Production Documentation
Complete technical reference for using Elefante (10 docs + README)

**Core Documentation**:
- [`architecture.md`](technical/architecture.md) - System design & triple-layer architecture
- [`cognitive-memory-model.md`](technical/cognitive-memory-model.md) - AI memory model
- [`installation.md`](technical/installation.md) - Installation guide
- [`usage.md`](technical/usage.md) - **Complete API reference (11 MCP tools)**
- [`dashboard.md`](technical/dashboard.md) - Visual knowledge graph guide

**Advanced Documentation**:
- [`installation-safeguards.md`](technical/installation-safeguards.md) - Automated safeguards
- [`memory-schema-v2.md`](technical/memory-schema-v2.md) - Database schema
- [`v2-schema-simple.md`](technical/v2-schema-simple.md) - Schema simplified
- [`technical-implementation.md`](technical/technical-implementation.md) - Implementation details
- [`walkthrough.md`](technical/walkthrough.md) - Step-by-step guide

**See**: [`technical/README.md`](technical/README.md) for complete index

---

### [`debug/`](debug/) - Development Documentation
Debugging, troubleshooting, and development logs (25 docs + README)

**By Topic**:
- **[`installation/`](debug/installation/)** (7 files) - Installation troubleshooting
  - [`never-again-guide.md`](debug/installation/never-again-guide.md) - Ultimate troubleshooting
  - [`installation-debug-2025-11-27.md`](debug/installation/installation-debug-2025-11-27.md) - Debug session
  - [`root-cause-analysis.md`](debug/installation/root-cause-analysis.md) - Cognitive failures

- **[`dashboard/`](debug/dashboard/)** (2 files) - Dashboard debugging
  - [`dashboard-build-failure-2025-11-28.md`](debug/dashboard/dashboard-build-failure-2025-11-28.md)
  - [`dashboard-postmortem.md`](debug/dashboard/dashboard-postmortem.md)

- **[`database/`](debug/database/)** (4 files) - Database issues
  - [`database-corruption-2025-12-02.md`](debug/database/database-corruption-2025-12-02.md)
  - [`kuzu-critical-discovery.md`](debug/database/kuzu-critical-discovery.md)
  - [`kuzu-lock-analysis.md`](debug/database/kuzu-lock-analysis.md)
  - [`duplicate-entity-analysis.md`](debug/database/duplicate-entity-analysis.md)

- **[`memory/`](debug/memory/)** (1 file) - Memory system debugging
  - [`memory-retrieval-investigation.md`](debug/memory/memory-retrieval-investigation.md)

- **[`general/`](debug/general/)** (11 files) - Planning & status
  - [`task-roadmap.md`](debug/general/task-roadmap.md) - 🎯 **Active feature roadmap**
  - [`implementation-plan.md`](debug/general/implementation-plan.md)
  - [`troubleshooting.md`](debug/general/troubleshooting.md)
  - [`dev-journal.md`](debug/general/dev-journal.md)
  - [`current-status.md`](debug/general/current-status.md)

**See**: [`debug/README.md`](debug/README.md) for complete index

---

### [`archive/`](archive/) - Historical Documentation
Preserved historical documents (12 files)

**Installation Archives** (7 files):
- Installation reports from 2025-11-27
- Historical troubleshooting logs
- Deployment debug logs

**v1.1.0 Cleanup Archives** (5 files):
- Archived duplicate documentation
- Historical MCP troubleshooting guides
- Consolidated project overviews

---

## 🔌 MCP Tools Reference

Elefante provides **11 MCP tools** for AI agents:

| Tool | Purpose |
|------|---------|
| `addMemory` | Store with intelligent ingestion (NEW/REDUNDANT/RELATED/CONTRADICTORY) |
| `searchMemories` | Hybrid search (semantic + structured + context) |
| `queryGraph` | Execute Cypher queries on knowledge graph |
| `getContext` | Get comprehensive session context |
| `createEntity` | Create nodes in knowledge graph |
| `createRelationship` | Link entities with relationships |
| `getEpisodes` | Browse past sessions with summaries |
| `getStats` | System health & usage statistics |
| `consolidateMemories` | Merge duplicates & resolve contradictions |
| `listAllMemories` | Export/inspect all memories (no filtering) |
| `openDashboard` | Launch visual Knowledge Garden UI |

**Complete API reference**: [`technical/usage.md`](technical/usage.md)

---

## 📖 Documentation by Use Case

### "I'm new to Elefante"
1. Read [`../README.md`](../README.md) - High-level overview
2. Follow [`technical/installation.md`](technical/installation.md) - Install
3. Try [`technical/walkthrough.md`](technical/walkthrough.md) - Hands-on guide
4. Explore [`technical/dashboard.md`](technical/dashboard.md) - Visual interface

### "I want to use the API"
1. Start with [`technical/usage.md`](technical/usage.md) - Complete API reference
2. Review [`technical/architecture.md`](technical/architecture.md) - Understand the system
3. Check [`technical/cognitive-memory-model.md`](technical/cognitive-memory-model.md) - Memory intelligence

### "I'm having problems"
1. Check [`debug/general/troubleshooting.md`](debug/general/troubleshooting.md) - Common issues
2. Review [`debug/installation/never-again-guide.md`](debug/installation/never-again-guide.md) - Installation help
3. Search [`debug/`](debug/) by topic (installation, dashboard, database, memory)

### "I want to contribute"
1. Read [`../CONTRIBUTING.md`](../CONTRIBUTING.md) - Guidelines
2. Check [`debug/general/task-roadmap.md`](debug/general/task-roadmap.md) - Active tasks
3. Review [`../NEXT_STEPS.md`](../NEXT_STEPS.md) - v1.2.0 roadmap
4. See [`../CHANGELOG.md`](../CHANGELOG.md) - Recent changes

---

## 🎯 Current Development Status

**Version**: v1.1.0 (Production)  
**Next**: v1.2.0 - Advanced Memory Intelligence Pipeline

**Priority Features** (from [`../NEXT_STEPS.md`](../NEXT_STEPS.md)):
- Enhanced LLM extraction
- Smart UPDATE (merge logic)
- Smart EXTEND (link logic)

**Active Roadmap**: [`debug/general/task-roadmap.md`](debug/general/task-roadmap.md)

---

## 📊 Documentation Statistics

- **Technical Docs**: 10 production documents
- **Debug Docs**: 25 development documents
- **Archive**: 12 historical documents
- **Total**: 47+ documents
- **MCP Tools**: 11 fully documented
- **Code Examples**: 50+ across all docs

---

## 🔍 Search Tips

**Looking for specific topics**:
- Installation → `technical/installation.md` or `debug/installation/`
- API/Tools → `technical/usage.md` (all 11 tools)
- Architecture → `technical/architecture.md`
- Dashboard → `technical/dashboard.md`
- Troubleshooting → `debug/general/troubleshooting.md`
- Roadmap → `debug/general/task-roadmap.md`

**File naming convention**: All files use kebab-case (lowercase-with-hyphens)

---

## 📝 Maintenance

**Last Updated**: 2025-12-03  
**Documentation Version**: v1.1.0  
**Status**: ✅ Complete and up-to-date

**Maintainers**: Elefante Core Team

---

**For the main project overview, see [`../README.md`](../README.md)**