# Elefante Deployment Guide

Complete step-by-step guide to deploy and test Elefante.

## Prerequisites

- Python 3.9 or higher
- Git installed
- GitHub account (for pushing code)
- ~2GB free disk space (for models and data)

---

## Step 1: Install Dependencies (5 minutes)

### Windows
```powershell
cd Elefante
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Linux/Mac
```bash
cd Elefante
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

### Expected Output
```
Successfully installed:
- pydantic
- pyyaml
- chromadb
- kuzu
- sentence-transformers
- mcp
- ... (and dependencies)
```

### Troubleshooting

**Issue: ChromaDB fails to install**
```bash
# Windows: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Linux: Install build essentials
sudo apt-get install build-essential python3-dev

# Mac: Install Xcode Command Line Tools
xcode-select --install
```

**Issue: Kuzu fails to install**
```bash
# Try installing from source
pip install kuzu --no-binary kuzu
```

**Issue: Sentence Transformers model download fails**
```bash
# Set cache directory
export TRANSFORMERS_CACHE=./models
# Or on Windows:
set TRANSFORMERS_CACHE=./models
```

---

## Step 2: Initialize Databases (2 minutes)

```bash
python scripts/init_databases.py
```

### Expected Output
```
============================================================
Elefante Database Initialization
============================================================

Initializing embedding service...
✓ Embedding service initialized
  model: all-MiniLM-L6-v2
  dimension: 384

Initializing ChromaDB vector store...
✓ Vector store initialized
  collection: memories
  count: 0

Initializing Kuzu graph database...
✓ Graph store initialized
  num_nodes: 0
  num_relationships: 0

Verifying system setup...
✓ Data directories verified

============================================================
Initialization Summary
============================================================
embedding_service    : ✓ SUCCESS
vector_store        : ✓ SUCCESS
graph_store         : ✓ SUCCESS
verification        : ✓ SUCCESS
============================================================
✓ All components initialized successfully!
============================================================
```

### Troubleshooting

**Issue: Permission denied creating directories**
```bash
# Create data directory manually
mkdir -p data/chroma data/kuzu logs
```

**Issue: Model download fails**
```bash
# Download model manually
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## Step 3: Run Health Check (1 minute)

```bash
python scripts/health_check.py
```

### Expected Output
```
============================================================
Elefante Health Check
Timestamp: 2024-01-15T10:30:00.000Z
============================================================

Checking Configuration...
✓ Configuration: HEALTHY
  - data_dir: ./data

Checking Embedding Service...
✓ Embedding Service: HEALTHY
  - model: all-MiniLM-L6-v2
  - dimension: 384

Checking Vector Store...
✓ Vector Store: HEALTHY
  - collection: memories
  - count: 0

Checking Graph Store...
✓ Graph Store: HEALTHY
  - nodes: 0
  - relationships: 0

Checking Orchestrator...
✓ Orchestrator: HEALTHY

============================================================
✓ All systems operational!
============================================================
```

---

## Step 4: Run End-to-End Tests (3 minutes)

```bash
python scripts/test_end_to_end.py
```

### Expected Output
```
============================================================
ELEFANTE END-TO-END VALIDATION TEST
Timestamp: 2024-01-15T10:35:00.000Z
============================================================

============================================================
TEST 1: Add Memory
============================================================
✓ Memory created: 12345678-1234-1234-1234-123456789abc
  Content: Elefante is a dual-database AI memory system...
  Type: fact
  Importance: 10
  Tags: ['elefante', 'architecture', 'database']

============================================================
TEST 2: Semantic Search
============================================================
✓ Found 1 results

  Result 1:
    Score: 0.892
    Content: Elefante is a dual-database AI memory system...
    Source: vector

============================================================
TEST 3: Hybrid Search
============================================================
✓ Found 1 results

  Result 1:
    Score: 0.850
    Vector Score: 0.892
    Graph Score: 0.800
    Content: Elefante is a dual-database AI memory system...

============================================================
TEST 4: Entity & Relationship Creation
============================================================
✓ Created entity: Bob (person)
✓ Created entity: Jaime (person)
✓ Created relationship: Bob -> Jaime

============================================================
TEST 5: Context Retrieval
============================================================
✓ Retrieved context:
  Memories: 1
  Entities: 5
  Depth: 2

============================================================
TEST 6: System Statistics
============================================================
✓ System Statistics:

  Vector Store:
    Collection: memories
    Count: 1

  Graph Store:
    Nodes: 5
    Relationships: 4

  Orchestrator:
    Status: operational

============================================================
TEST SUMMARY
============================================================
add_memory          : ✓ PASS
semantic_search     : ✓ PASS
hybrid_search       : ✓ PASS
entity_creation     : ✓ PASS
get_context         : ✓ PASS
system_stats        : ✓ PASS

============================================================
Results: 6 passed, 0 failed
============================================================

🎉 ALL TESTS PASSED!
Elefante is working end-to-end!

Next steps:
1. Start MCP server: python -m src.mcp.server
2. Configure your IDE to use Elefante
3. Start using persistent AI memory!
```

---

## Step 5: Start MCP Server (Optional)

```bash
python -m src.mcp.server
```

### Expected Output
```
INFO: Elefante MCP Server initialized
INFO: Starting Elefante MCP Server...
INFO: MCP Server running on stdio
```

### Configure IDE

**For Cline/Cursor:**
1. Open IDE settings
2. Add MCP server configuration:
```json
{
  "mcpServers": {
    "elefante": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "cwd": "/path/to/Elefante"
    }
  }
}
```

---

## Step 6: Push to GitHub

### Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `elefante`
3. Description: "Dual-database AI memory system with hybrid intelligence"
4. Visibility: Public or Private
5. Click "Create repository"

### Push Code
```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/elefante.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Expected Output
```
Enumerating objects: 150, done.
Counting objects: 100% (150/150), done.
Delta compression using up to 8 threads
Compressing objects: 100% (120/120), done.
Writing objects: 100% (150/150), 250.00 KiB | 5.00 MiB/s, done.
Total 150 (delta 45), reused 0 (delta 0)
To https://github.com/YOUR_USERNAME/elefante.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Verification Checklist

- [ ] Dependencies installed successfully
- [ ] Databases initialized without errors
- [ ] Health check shows all systems healthy
- [ ] All 6 end-to-end tests pass
- [ ] MCP server starts without errors
- [ ] Code pushed to GitHub successfully

---

## Troubleshooting Common Issues

### Import Errors
```bash
# Ensure you're in the Elefante directory
cd Elefante

# Verify Python can find modules
python -c "import src.core.orchestrator"
```

### Database Errors
```bash
# Clear and reinitialize
rm -rf data/
python scripts/init_databases.py
```

### Performance Issues
```bash
# Check system resources
# ChromaDB and Kuzu need ~1GB RAM
# Sentence Transformers need ~500MB RAM
```

---

## Next Steps After Deployment

1. **Use Elefante in your IDE**
   - Configure MCP server
   - Start storing memories
   - Test hybrid search

2. **Customize Configuration**
   - Edit `config.yaml`
   - Adjust importance thresholds
   - Configure embedding model

3. **Monitor Performance**
   - Check logs in `logs/`
   - Monitor database sizes
   - Track search performance

4. **Contribute**
   - Report issues on GitHub
   - Submit pull requests
   - Share your use cases

---

## Support

- **Documentation**: See README.md and ARCHITECTURE.md
- **Issues**: Create GitHub issue
- **Questions**: Check ARCHITECTURE.md FAQ section

---

**Deployment Guide v1.0 - Made with Bob** 🐘