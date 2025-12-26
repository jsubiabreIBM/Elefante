# Elefante Test Suite

> **Version:** 1.1.0  
> **Last Updated:** 2025-12-26

## Overview

Critical regression tests only. Stable/completed features archived.

## Quick Start

```bash
# Run all critical tests
pytest tests/ -v
```

---

## Active Tests (4 critical)

| File | Purpose |
|------|---------|
| `test_memory_persistence.py` | **CRITICAL** - Ensures DB writes persist |
| `test_test_memory_guard.py` | **CRITICAL** - Prevents test pollution |
| `test_scoring.py` | Active development - scoring logic |
| `test_refinery.py` | Active development - memory refinery |
| `verification/test_mcp_server.py` | MCP server smoke test |

---

## Directory Structure

```
tests/
├── README.md
├── conftest.py               # Shared fixtures
├── pytest.ini                # pytest config
├── test_memory_persistence.py # CRITICAL
├── test_test_memory_guard.py  # CRITICAL
├── test_scoring.py            # Active
├── test_refinery.py           # Active
├── archive/                   # Stable feature tests (reference only)
├── manual/                    # Manual verification scripts
└── verification/              # CI smoke tests
```

## Archive

Stable/completed feature tests - run if needed:
```bash
pytest tests/archive/ -v
```

---

## Made with Bob 🐘
