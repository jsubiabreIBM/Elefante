# 🐘 Elefante IDE Integration Guide

## How to Use Elefante While Working in Your IDE

Elefante integrates with Claude Desktop (and other MCP-compatible IDEs) to give your AI assistant persistent memory. Here's how to set it up:

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start the Elefante MCP Server

Open a terminal in the Elefante directory and run:

```bash
cd C:\Users\JaimeSubiabreCistern\Documents\Agentic\Elefante
python -m src.mcp.server
```

**Keep this terminal running!** The server needs to stay active for Claude Desktop to use it.

You should see:
```
INFO: Elefante MCP server starting...
INFO: Server ready on stdio
```

---

### Step 2: Configure Claude Desktop

1. **Find Claude Desktop config file**:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Full path: `C:\Users\JaimeSubiabreCistern\AppData\Roaming\Claude\claude_desktop_config.json`

2. **Edit the config file** (create it if it doesn't exist):

```json
{
  "mcpServers": {
    "elefante": {
      "command": "python",
      "args": [
        "-m",
        "src.mcp.server"
      ],
      "cwd": "C:\\Users\\JaimeSubiabreCistern\\Documents\\Agentic\\Elefante",
      "env": {
        "PYTHONPATH": "C:\\Users\\JaimeSubiabreCistern\\Documents\\Agentic\\Elefante"
      }
    }
  }
}
```

3. **Restart Claude Desktop** completely (close and reopen)

---

### Step 3: Verify Connection

In Claude Desktop, you should see:
- 🔌 A "Connected" indicator for Elefante
- 🛠️ 7 new tools available in the tools menu

---

## 🎯 How to Use Elefante in Your Workflow

### 1. **Store Important Information**

While coding, tell Claude to remember things:

```
"Remember that I prefer using async/await over callbacks in Python"
"Store this: My API key naming convention is {service}_API_KEY"
"Remember: I'm working on the Elefante project, a dual-database AI memory system"
```

Claude will use the `addMemory` tool to store this in Elefante.

---

### 2. **Retrieve Context**

Ask Claude to recall information:

```
"What do you remember about my coding preferences?"
"What projects am I working on?"
"What do you know about my API key conventions?"
```

Claude will use `searchMemories` to find relevant information.

---

### 3. **Build Knowledge Graphs**

Create relationships between concepts:

```
"Remember that Elefante uses ChromaDB and Kuzu databases"
"Store that I work at IBM in Toronto"
"Remember: Bob is the AI assistant helping me build Elefante"
```

Elefante automatically creates entity relationships in the graph database.

---

### 4. **Query Your Knowledge Graph**

Ask structured questions:

```
"Show me all technologies I've worked with"
"What are all the projects related to AI?"
"Find all people I've mentioned in conversations"
```

Claude will use `queryGraph` to traverse relationships.

---

## 🛠️ Available Tools in Claude Desktop

Once connected, Claude can use these 7 tools:

| Tool | Purpose | Example Use |
|------|---------|-------------|
| `addMemory` | Store new information | "Remember my coding style preferences" |
| `searchMemories` | Find relevant memories | "What do you know about my projects?" |
| `getMemory` | Retrieve specific memory by ID | Internal use by Claude |
| `updateMemory` | Modify existing memory | "Update my email address" |
| `deleteMemory` | Remove a memory | "Forget that old API key" |
| `queryGraph` | Search knowledge graph | "Show all technologies I use" |
| `getSystemStats` | Check Elefante health | "How many memories do I have?" |

---

## 💡 Real-World Usage Examples

### Example 1: Project Context
```
You: "I'm starting work on the authentication module"
Claude: [Uses searchMemories to find related context]
Claude: "I remember you're working on Elefante. Should I recall 
        your preferred authentication patterns?"
```

### Example 2: Code Preferences
```
You: "Write a function to fetch user data"
Claude: [Checks memories for your coding style]
Claude: "Based on your preference for async/await, here's the function..."
```

### Example 3: Relationship Queries
```
You: "What technologies am I using in my current projects?"
Claude: [Uses queryGraph]
Claude: "You're using ChromaDB and Kuzu in Elefante, and working 
        with Python, MCP, and sentence-transformers."
```

---

## 🔧 Troubleshooting

### Server Won't Start
```bash
# Check Python environment
python --version  # Should be 3.11+

# Verify dependencies
pip install -r requirements.txt

# Check for port conflicts
netstat -ano | findstr :5000
```

### Claude Desktop Not Connecting

1. **Check config file syntax** (must be valid JSON)
2. **Verify paths** (use double backslashes `\\` on Windows)
3. **Restart Claude Desktop** completely
4. **Check logs**:
   - Windows: `%APPDATA%\Claude\logs\`

### Memory Not Persisting

```bash
# Check database directories exist
dir data\chroma
dir data\kuzu

# Run health check
python scripts\health_check.py
```

---

## 🎨 Advanced Usage

### Custom Memory Types

```python
# In your conversations, specify memory types:
"Remember this as a FACT: Python 3.11 is my default version"
"Store as PREFERENCE: I prefer dark mode in all IDEs"
"Save as CONVERSATION: Discussed async patterns with Bob today"
```

### Importance Levels

```python
# Higher importance = retrieved more often
"Remember (CRITICAL): Production API key is in .env file"
"Remember (HIGH): I'm on EST timezone (UTC-5)"
"Remember (NORMAL): I like coffee in the morning"
```

### Tags for Organization

```python
"Remember: Use pytest for testing [tags: python, testing, best-practices]"
"Store: API rate limit is 100 req/min [tags: api, limits, production]"
```

---

## 📊 Monitoring Your Memory

### Check System Stats
```
You: "How many memories do I have?"
Claude: [Uses getSystemStats]
Claude: "You have 16 memories stored:
         - Vector store: 16 memories
         - Graph store: 25 entities, 30 relationships
         - System status: operational"
```

### Search by Type
```
You: "Show me all my coding preferences"
Claude: [Searches with type filter]
```

---

## 🔐 Privacy & Security

✅ **Fully Local**: All data stays on your machine
✅ **No Cloud**: No external API calls for memory storage
✅ **Encrypted**: Can add encryption layer if needed
✅ **Portable**: Copy `data/` folder to backup/transfer

---

## 🚀 Next Steps

1. ✅ Start the MCP server (Step 1)
2. ✅ Configure Claude Desktop (Step 2)
3. ✅ Test with: "Remember that I'm Jaime, an IBM developer in Toronto"
4. ✅ Query with: "What do you know about me?"
5. 🎉 Enjoy persistent AI memory in your IDE!

---

## 📚 Additional Resources

- **Architecture**: See `ARCHITECTURE.md` for system design
- **API Reference**: See `src/mcp/server.py` for tool schemas
- **Deployment**: See `DEPLOYMENT_GUIDE.md` for production setup
- **Quick Start**: See `QUICK_START.md` for basic usage

---

## 🆘 Need Help?

If you encounter issues:

1. Check the MCP server logs (terminal output)
2. Run health check: `python scripts/health_check.py`
3. Run tests: `python scripts/test_end_to_end.py`
4. Check Claude Desktop logs in `%APPDATA%\Claude\logs\`

---

**🐘 Elefante - Your AI's Persistent Memory System**

*Built by Jaime Subiabre Cisterna*
*IBM Developer, Toronto, Canada*