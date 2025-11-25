# 🐘 Elefante Setup for VSCode/Bob

## Auto-Start Elefante with Bob AI Assistant

This guide shows you how to configure Elefante to **automatically start** every time you open VSCode/Bob, giving your AI assistant persistent memory.

---

## ⚡ ONE-CLICK SETUP

### Step 1: Run Configuration Script

```bash
cd C:\Users\JaimeSubiabreCistern\Documents\Agentic\Elefante
python configure_vscode_bob.py
```

This script will:
- ✅ Add Elefante to your VSCode MCP servers
- ✅ Enable auto-start (launches when VSCode opens)
- ✅ Configure all necessary paths

### Step 2: Restart VSCode/Bob

Close and reopen VSCode/Bob completely.

### Step 3: Verify Connection

Open the AI assistant panel and you should see:
- 🔌 Elefante connected
- 🛠️ 7 new tools available

**That's it!** Elefante now auto-starts with Bob.

---

## 🎯 HOW TO USE WITH BOB

### Storing Information

Just tell Bob to remember things naturally:

```
You: "Remember that I prefer async/await over callbacks in Python"
Bob: [Uses addMemory tool] ✅ Stored in Elefante

You: "Store this: My API naming convention is {service}_API_KEY"
Bob: [Uses addMemory tool] ✅ Stored in Elefante

You: "Remember I'm working on Elefante, a dual-database AI memory system"
Bob: [Uses addMemory tool] ✅ Stored in Elefante
```

### Retrieving Information

Ask Bob to recall information:

```
You: "What do you remember about my coding preferences?"
Bob: [Uses searchMemories tool]
     "You prefer async/await over callbacks in Python..."

You: "What projects am I working on?"
Bob: [Uses searchMemories tool]
     "You're working on Elefante, a dual-database AI memory system..."

You: "What's my API key naming convention?"
Bob: [Uses searchMemories tool]
     "Your convention is {service}_API_KEY..."
```

### Querying Relationships

Ask about connections between concepts:

```
You: "Show me all technologies I'm using"
Bob: [Uses queryGraph tool]
     "ChromaDB, Kuzu, Python, MCP, sentence-transformers..."

You: "What are all my projects related to AI?"
Bob: [Uses queryGraph tool]
     "Elefante (AI memory system), Autogen projects..."
```

---

## 🛠️ Available Tools

Bob can now use these 7 Elefante tools automatically:

| Tool | Purpose | When Bob Uses It |
|------|---------|------------------|
| `addMemory` | Store information | When you say "remember" or "store" |
| `searchMemories` | Find memories | When you ask "what do you know" |
| `getMemory` | Get specific memory | Internal use by Bob |
| `updateMemory` | Modify memory | When you say "update" or "change" |
| `deleteMemory` | Remove memory | When you say "forget" |
| `queryGraph` | Search relationships | When you ask "show all" or "find" |
| `getSystemStats` | Check health | When you ask "how many memories" |

---

## 💡 Real-World Examples

### Example 1: Code Style Memory
```
You: "I'm writing a new API endpoint"
Bob: [Searches memories for your coding style]
Bob: "I remember you prefer async/await and type hints. 
      Here's the endpoint following your style..."
```

### Example 2: Project Context
```
You: "What was I working on yesterday?"
Bob: [Searches memories by date]
Bob: "You were debugging the Kuzu relationship property 
      issue in Elefante's graph store"
```

### Example 3: Technology Stack
```
You: "What databases am I using in my projects?"
Bob: [Queries knowledge graph]
Bob: "In Elefante: ChromaDB (vector) and Kuzu (graph).
      In other projects: PostgreSQL, Redis..."
```

---

## 📊 Current Memory Status

Your Elefante already has **16 memories** including:

### About You:
- Name: Jaime Subiabre Cisterna
- Company: IBM
- Location: Toronto, Canada
- Role: Developer (AI & Automation)

### About Elefante:
- Dual-database system (ChromaDB + Kuzu)
- MCP integration for VSCode/Bob
- 7 tools for memory operations
- All 6 tests passing

### Technical Stack:
- Python 3.11
- sentence-transformers for embeddings
- 384-dimensional vectors
- Automatic entity relationship creation

---

## 🔧 Configuration Details

The script adds this to your VSCode `settings.json`:

```json
{
  "chat.mcp.gallery.enabled": true,
  "chat.mcp.servers": {
    "elefante": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "cwd": "C:\\Users\\JaimeSubiabreCistern\\Documents\\Agentic\\Elefante",
      "env": {
        "PYTHONPATH": "C:\\Users\\JaimeSubiabreCistern\\Documents\\Agentic\\Elefante"
      },
      "autoStart": true
    }
  }
}
```

**Key Setting**: `"autoStart": true` - This makes Elefante start automatically!

---

## 🔍 Troubleshooting

### Elefante Not Auto-Starting?

1. **Check VSCode settings**:
   - Open: `File > Preferences > Settings`
   - Search: "mcp"
   - Verify: `chat.mcp.gallery.enabled` is `true`

2. **Check MCP servers**:
   - Open Command Palette (`Ctrl+Shift+P`)
   - Type: "MCP: Show Servers"
   - Verify: Elefante is listed and enabled

3. **Check logs**:
   - Open: `View > Output`
   - Select: "MCP" from dropdown
   - Look for Elefante startup messages

### Bob Not Using Elefante?

1. **Verify connection**:
   ```
   You: "How many memories do I have?"
   Bob: [Should use getSystemStats tool]
   ```

2. **Test manually**:
   ```
   You: "Use the addMemory tool to store: Test memory"
   Bob: [Should explicitly use the tool]
   ```

3. **Restart VSCode**:
   - Close completely
   - Reopen
   - Wait 10 seconds for auto-start

### Python Errors?

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
cd C:\Users\JaimeSubiabreCistern\Documents\Agentic\Elefante
pip install -r requirements.txt

# Test manually
python -m src.mcp.server
```

---

## 🎨 Advanced Usage

### Memory Types

Specify memory types for better organization:

```
"Remember as FACT: Python 3.11 is my default version"
"Store as PREFERENCE: I prefer dark mode in all IDEs"
"Save as CONVERSATION: Discussed async patterns with Bob"
```

### Importance Levels

Higher importance = retrieved more often:

```
"Remember (CRITICAL): Production API key is in .env file"
"Remember (HIGH): I'm on EST timezone (UTC-5)"
"Remember (NORMAL): I like coffee in the morning"
```

### Tags

Organize memories with tags:

```
"Remember: Use pytest for testing [tags: python, testing, best-practices]"
"Store: API rate limit is 100 req/min [tags: api, limits, production]"
```

---

## 📈 Monitoring

### Check System Health

```
You: "How many memories do I have?"
Bob: [Uses getSystemStats]
     "16 memories in vector store, 25 entities in graph"

You: "Is Elefante working properly?"
Bob: [Uses getSystemStats]
     "Status: operational, all systems healthy"
```

### View Recent Memories

```
You: "What did we discuss recently?"
Bob: [Searches with date filter]
     "Recent conversations about Kuzu debugging, MCP setup..."
```

---

## 🔐 Privacy & Security

✅ **100% Local**: All data stays on your machine
✅ **No Cloud**: No external API calls for memory
✅ **Private**: Only you and Bob can access memories
✅ **Portable**: Copy `data/` folder to backup

**Data Location**: `C:\Users\JaimeSubiabreCistern\Documents\Agentic\Elefante\data\`

---

## 🚀 Quick Test

After setup, test with these commands:

1. **Store a memory**:
   ```
   "Remember that I'm Jaime, an IBM developer in Toronto"
   ```

2. **Retrieve it**:
   ```
   "What do you know about me?"
   ```

3. **Check stats**:
   ```
   "How many memories do I have?"
   ```

If all three work, Elefante is fully operational! 🎉

---

## 📚 Additional Resources

- **Architecture**: `ARCHITECTURE.md` - System design details
- **API Reference**: `src/mcp/server.py` - Tool schemas
- **Testing**: `test_real_memories.py` - Real-world test
- **Health Check**: `scripts/health_check.py` - System diagnostics

---

## 🆘 Need Help?

1. **Run health check**:
   ```bash
   python scripts/health_check.py
   ```

2. **Run tests**:
   ```bash
   python scripts/test_end_to_end.py
   ```

3. **Check logs**:
   - VSCode: `View > Output > MCP`
   - Elefante: `logs/` directory

4. **Manual start** (for debugging):
   ```bash
   python -m src.mcp.server
   ```

---

## ✅ Success Checklist

- [ ] Ran `configure_vscode_bob.py`
- [ ] Restarted VSCode/Bob
- [ ] See Elefante in MCP servers list
- [ ] Tested: "Remember that I'm Jaime"
- [ ] Tested: "What do you know about me?"
- [ ] Bob successfully uses Elefante tools

---

**🐘 Elefante - Persistent Memory for Bob AI Assistant**

*Auto-starts with VSCode/Bob*
*Fully local and private*
*16 memories already stored*

*Built by Jaime Subiabre Cisterna*
*IBM Developer, Toronto, Canada*