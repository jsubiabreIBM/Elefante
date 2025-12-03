# Elefante Documentation Index

Complete guide to all documentation in the Elefante repository.

---

## 🚀 Getting Started (Start Here!)

| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](README.md) | Project overview and quick start | Everyone |
| [docs/SETUP.md](docs/SETUP.md) | Manual installation guide | New users |
| [docs/IDE_SETUP.md](docs/IDE_SETUP.md) | Connect to VS Code/Cursor/Claude | Developers |
| [docs/TUTORIAL.md](docs/TUTORIAL.md) | Hands-on walkthrough | New users |

---

## 📊 Dashboard & Visualization

| Document | Purpose | Audience |
|----------|---------|----------|
| [docs/DASHBOARD.md](docs/DASHBOARD.md) | Complete dashboard usage guide | All users |
| [DEBUG/DASHBOARD_DEBUGGING_POSTMORTEM.md](DEBUG/DASHBOARD_DEBUGGING_POSTMORTEM.md) | Debugging lessons learned | Maintainers |

**Quick Start:**
```bash
cd Elefante
.venv\Scripts\python.exe -m src.dashboard.server
# Open http://127.0.0.1:8000
```

---

## 🔧 Technical Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | High-level system design | Developers |
| [docs/ARCHITECTURE_DEEP_DIVE.md](docs/ARCHITECTURE_DEEP_DIVE.md) | Detailed technical analysis | Advanced developers |
| [docs/API.md](docs/API.md) | Complete API reference | Developers |
| [docs/STRUCTURE.md](docs/STRUCTURE.md) | Project directory layout | Contributors |
| [TECHNICAL_IMPLEMENTATION_DETAILS.md](TECHNICAL_IMPLEMENTATION_DETAILS.md) | Implementation specifics | Maintainers |

---

## 🛠️ Installation & Setup

| Document | Purpose | Audience |
|----------|---------|----------|
| [INSTALLATION_SAFEGUARDS.md](INSTALLATION_SAFEGUARDS.md) | Automated prevention system | Maintainers |
| [NEVER_AGAIN_COMPLETE_GUIDE.md](NEVER_AGAIN_COMPLETE_GUIDE.md) | Ultimate troubleshooting guide | Support |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues and fixes | All users |

---

## 🧪 Testing & Quality

| Document | Purpose | Audience |
|----------|---------|----------|
| [docs/TESTING.md](docs/TESTING.md) | How to run test suite | Developers |
| [tests/integration/](tests/integration/) | Integration test files | Developers |

**Run Tests:**
```bash
cd Elefante
.venv\Scripts\python.exe -m pytest tests/
```

---

## 📝 Project Management

| Document | Purpose | Audience |
|----------|---------|----------|
| [CHANGELOG.md](CHANGELOG.md) | Version history and changes | Everyone |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines | Contributors |
| [LICENSE](LICENSE) | MIT License terms | Everyone |

---

## 🗂️ Archived Documentation

Historical documents preserved for reference (not actively maintained):

### Installation & Setup Archives
| Document | Original Purpose | Date Archived |
|----------|-----------------|---------------|
| [docs/archive/INSTALLATION_COMPLETE_REPORT_2025-11-27.md](docs/archive/INSTALLATION_COMPLETE_REPORT_2025-11-27.md) | Installation report | 2024-11-29 |
| [docs/archive/INSTALLATION_COMPLETE_REPORT.md](docs/archive/INSTALLATION_COMPLETE_REPORT.md) | Installation report | 2024-11-29 |
| [docs/archive/MISSION_ACCOMPLISHED_SUMMARY.md](docs/archive/MISSION_ACCOMPLISHED_SUMMARY.md) | Project summary | 2024-11-29 |
| [docs/archive/INSTALLATION_LOG.md](docs/archive/INSTALLATION_LOG.md) | Installation log | 2024-11-29 |
| [docs/archive/INSTALLATION_TRACKER.md](docs/archive/INSTALLATION_TRACKER.md) | Installation tracker | 2024-11-29 |
| [docs/archive/TROUBLESHOOTING_LOG.md](docs/archive/TROUBLESHOOTING_LOG.md) | Troubleshooting log | 2024-11-29 |
| [docs/archive/DEPLOYMENT_DEBUG_LOG.md](docs/archive/DEPLOYMENT_DEBUG_LOG.md) | Deployment log | 2024-11-29 |

### v1.1.0 Cleanup Archives (2025-12-03)
| Document | Original Purpose | Reason Archived |
|----------|-----------------|-----------------|
| [docs/archive/COMPLETE_DOCUMENTATION_INDEX.md](docs/archive/COMPLETE_DOCUMENTATION_INDEX.md) | Documentation index | Duplicate of DOCUMENTATION_INDEX.md |
| [docs/archive/MCP_ENABLED_SOLUTION.md](docs/archive/MCP_ENABLED_SOLUTION.md) | MCP database lock fix | Historical fix, issue resolved |
| [docs/archive/MCP_FIX_DOCUMENTATION.md](docs/archive/MCP_FIX_DOCUMENTATION.md) | MCP troubleshooting | Overlaps with main troubleshooting |
| [docs/archive/MCP_TROUBLESHOOTING_GUIDE.md](docs/archive/MCP_TROUBLESHOOTING_GUIDE.md) | MCP troubleshooting | Consolidated into main docs |
| [docs/archive/ZLCTP_PROJECT_DOCUMENTATION.md](docs/archive/ZLCTP_PROJECT_DOCUMENTATION.md) | Project overview | Content overlaps with README |

---

## 🛠️ Utility Scripts

### Memory Management
| Script | Purpose | Location |
|--------|---------|----------|
| `add_memories.py` | Batch add memories | `scripts/utils/` |
| `add_debugging_lessons.py` | Add debugging insights | `scripts/utils/` |
| `verify_memories.py` | Verify stored memories | `scripts/utils/` |
| `manual_test_memory_persistence.py` | Manual persistence testing | `scripts/utils/` |

### Dashboard Management
| Script | Purpose | Location |
|--------|---------|----------|
| `restart_dashboard.bat` | Clean dashboard restart | `scripts/dashboard/` |

### Debug Tools
| Script | Purpose | Location |
|--------|---------|----------|
| `auto_repair_chromadb.py` | Repair ChromaDB issues | `scripts/debug/` |
| `inspect_chromadb.py` | Inspect ChromaDB structure | `scripts/debug/` |
| `repair_chromadb.py` | Manual ChromaDB repair | `scripts/debug/` |
| `nuclear_reset_kuzu.py` | Reset Kuzu database | `scripts/debug/` |
| `remove_kuzu_lock.py` | Remove Kuzu lock file | `scripts/debug/` |
| `fix_segments_table.py` | Fix ChromaDB segments | `scripts/debug/` |
| `test_tools.py` | Test MCP tools | `scripts/debug/` |

---

## 📋 Quick Reference

### Common Tasks
- **Install**: Run `install.bat` (Windows) or `./install.sh` (Mac/Linux)
- **Start Dashboard**: `.venv\Scripts\python.exe -m src.dashboard.server`
- **Run Tests**: `.venv\Scripts\python.exe -m pytest tests/`
- **Verify Memories**: `.venv\Scripts\python.exe scripts/utils/verify_memories.py`

### Getting Help
1. Check [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues
2. Review [NEVER_AGAIN_COMPLETE_GUIDE.md](NEVER_AGAIN_COMPLETE_GUIDE.md) for installation problems
3. Search [DEBUG/](DEBUG/) folder for post-mortem analysis
4. Check archived docs in [docs/archive/](docs/archive/) for historical context

---

**Last Updated**: 2025-12-03 (v1.1.0 Release)
| `add_memories.py` | Batch add memories | [scripts/utils/](scripts/utils/add_memories.py) |
| `add_debugging_lessons.py` | Add debugging insights | [scripts/utils/](scripts/utils/add_debugging_lessons.py) |
| `restart_dashboard.bat` | Clean dashboard restart | [scripts/dashboard/](scripts/dashboard/restart_dashboard.bat) |

---

## 📚 Documentation by Use Case

### "I want to install Elefante"
1. Start with [README.md](README.md) - Quick Start section
2. Run `install.bat` (Windows) or `install.sh` (Mac/Linux)
3. If issues occur, see [NEVER_AGAIN_COMPLETE_GUIDE.md](NEVER_AGAIN_COMPLETE_GUIDE.md)

### "I want to use the dashboard"
1. Read [docs/DASHBOARD.md](docs/DASHBOARD.md)
2. Start server: `.venv\Scripts\python.exe -m src.dashboard.server`
3. Open http://127.0.0.1:8000

### "I want to understand the architecture"
1. Start with [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. Deep dive: [docs/ARCHITECTURE_DEEP_DIVE.md](docs/ARCHITECTURE_DEEP_DIVE.md)
3. API reference: [docs/API.md](docs/API.md)

### "I want to contribute"
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Review [docs/STRUCTURE.md](docs/STRUCTURE.md)
3. Check [docs/TESTING.md](docs/TESTING.md)
4. See [CHANGELOG.md](CHANGELOG.md) for recent changes

### "I'm having problems"
1. Check [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
2. Review [NEVER_AGAIN_COMPLETE_GUIDE.md](NEVER_AGAIN_COMPLETE_GUIDE.md)
3. For dashboard issues: [DEBUG/DASHBOARD_DEBUGGING_POSTMORTEM.md](DEBUG/DASHBOARD_DEBUGGING_POSTMORTEM.md)

### "I want to integrate with my IDE"
1. Follow [docs/IDE_SETUP.md](docs/IDE_SETUP.md)
2. Configure MCP server settings
3. Test with [docs/TUTORIAL.md](docs/TUTORIAL.md) examples

---

## 📊 Documentation Statistics

- **Total Documents**: 20+ active documents
- **Archived Documents**: 7 historical references
- **Code Examples**: 50+ across tutorials and API docs
- **Test Coverage**: 73+ tests documented
- **Last Updated**: 2024-11-29

---

## 🔍 Quick Search Guide

**Looking for...**
- Installation help → [README.md](README.md), [NEVER_AGAIN_COMPLETE_GUIDE.md](NEVER_AGAIN_COMPLETE_GUIDE.md)
- Dashboard usage → [docs/DASHBOARD.md](docs/DASHBOARD.md)
- API reference → [docs/API.md](docs/API.md)
- Architecture → [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Troubleshooting → [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- Contributing → [CONTRIBUTING.md](CONTRIBUTING.md)
- Version history → [CHANGELOG.md](CHANGELOG.md)

---

## 📞 Support Channels

1. **Documentation**: Start with this index
2. **GitHub Issues**: For bugs and feature requests
3. **Discussions**: For questions and community support

---

**Last Updated**: 2024-11-29  
**Maintained By**: Elefante Core Team