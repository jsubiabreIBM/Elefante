# Install Escape Scripts (2025-12-11)

**Date:** 2025-12-11  
**Context:** Broken venv escape debugging session  
**Related:** `docs/debug/installation/installation-compendium.md` Issue #5

---

## Problem

During Dec 11 installation, the workspace virtual environment became corrupted:
- `.venv` was created with wrong Python version or corrupted state
- VS Code/Copilot agent was running Python from the broken `.venv`
- Standard `scripts/install.py` could not execute
- Circular dependency: Can't fix environment from within broken environment

## Solution Progression

Each script represents a different "escape hatch" strategy:

| Script | Strategy | Why It Was Tried |
|--------|----------|------------------|
| `RUN_INSTALL.py` | Wrapper calling DO_INSTALL | Initial attempt to delegate |
| `DO_INSTALL.py` | Minimal 50-line script | Reduce complexity, avoid imports |
| `AUTONOMOUS_INSTALL.py` | Full logging to file | Track what's happening |
| `NUCLEAR_INSTALL.py` | Script-as-string via subprocess | Escape via process inception |
| `DIRECT_INSTALL.py` | Shebang `#!/usr/bin/env python3.11` | Force system Python at OS level |
| `autonomous_fix.py` | Production-ready with retries | Best practices version |

## Key Insight

**The winning strategy**: Use subprocess to call system Python with absolute path:
```python
subprocess.run(["/opt/homebrew/bin/python3.11", "-c", "script..."])
```

This escapes the broken workspace environment entirely.

## Files

- `AUTONOMOUS_INSTALL.py` - Full-featured with logging
- `DIRECT_INSTALL.py` - Final successful approach (shebang)
- `DO_INSTALL.py` - Minimal version
- `NUCLEAR_INSTALL.py` - Embedded script-in-string
- `RUN_INSTALL.py` - Simple wrapper
- `autonomous_fix.py` - Production-ready version
- `emergency_fix.sh` - Shell script variant
- `install_daemon.sh` - Background daemon attempt

## Extracted Law

See `docs/debug/installation-neural-register.md` **LAW #12: Broken Venv Escape Protocol**

---

**Archived:** 2025-12-11  
**Reason:** Session artifacts documenting debugging progression
