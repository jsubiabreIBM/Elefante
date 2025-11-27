# Elefante Testing Guide

## 🚀 Automated Testing (Recommended)

The most reliable way to verify your installation is using the included test suite.

### Run Full System Check

```bash
python scripts/test_end_to_end.py
```

**What it tests:**

- ✅ Adding memories
- ✅ Semantic search
- ✅ Hybrid search
- ✅ Entity creation
- ✅ Context retrieval
- ✅ System stats

### Run Health Check

```bash
python scripts/health_check.py
```

**What it tests:**

- ✅ Database connectivity
- ✅ Configuration validity
- ✅ Embedding model status

---

## 🛠️ Manual Testing (Debugging)

If you need to debug specific MCP tools, you can use these JSON payloads in your MCP client (or via `curl` if running an HTTP wrapper).

### 1. Add Memory

```json
{
  "name": "addMemory",
  "arguments": {
    "content": "Jaime prefers PostgreSQL for production databases",
    "memory_type": "fact",
    "importance": 8
  }
}
```

### 2. Search Memory

```json
{
  "name": "searchMemories",
  "arguments": {
    "query": "What database does Jaime prefer?",
    "mode": "hybrid"
  }
}
```

### 3. Query Graph

```json
{
  "name": "queryGraph",
  "arguments": {
    "cypher_query": "MATCH (m:Entity {type: 'memory'}) RETURN m LIMIT 5"
  }
}
```

---

## 🧪 Running Unit Tests

For developers contributing to the codebase:

```bash
# Run all unit tests
pytest tests/ -v

# Run specific test file
pytest tests/test_orchestrator.py -v
```
