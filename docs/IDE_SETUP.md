# 🐘 Elefante IDE Integration Guide

## How to Connect Elefante to Your IDE

Elefante integrates with **Bob**, **VS Code**, **Cursor**, and **Claude Desktop** via the Model Context Protocol (MCP).

---

## 🚀 Automatic Configuration (Recommended)

We provide a script that automatically detects your IDE settings and injects the correct configuration.

1.  **Run the configuration script:**

    ```bash
    python scripts/configure_vscode_bob.py
    ```

2.  **Restart your IDE.**

That's it! Elefante will now auto-start whenever you open your IDE.

---

## 🛠️ Manual Configuration

If the script doesn't work for your specific setup, you can configure it manually.

### 1. VS Code / Bob (with MCP Extension)

Add this to your `settings.json`:

```json
{
  "mcpServers": {
    "elefante": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "cwd": "/absolute/path/to/Elefante",
      "env": {
        "PYTHONPATH": "/absolute/path/to/Elefante"
      },
      "autoStart": true
    }
  }
}
```

### 2. Claude Desktop

Edit `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac):

```json
{
  "mcpServers": {
    "elefante": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "cwd": "/absolute/path/to/Elefante",
      "env": {
        "PYTHONPATH": "/absolute/path/to/Elefante"
      }
    }
  }
}
```

---

## 🎯 How to Use Elefante

Once connected, you can use natural language to interact with your memory system.

### 1. Store Information

> "Remember that I prefer using async/await over callbacks."
> "Store this: My API key naming convention is {service}\_API_KEY."

### 2. Retrieve Context

> "What do you remember about my coding preferences?"
> "What projects am I working on?"

### 3. Query Knowledge Graph

> "Show me all technologies related to the Elefante project."

---

## 🛠️ Available Tools

| Tool                 | Purpose                | Example                     |
| -------------------- | ---------------------- | --------------------------- |
| `addMemory`          | Store new information  | "Remember X..."             |
| `searchMemories`     | Find relevant memories | "What do you know about X?" |
| `queryGraph`         | Execute Cypher queries | "Show relationships..."     |
| `getContext`         | Get session context    | (Auto-called by agent)      |
| `createEntity`       | Manually add entity    | "Create entity Bob..."      |
| `createRelationship` | Manually link entities | "Link Bob to Project..."    |

---

## 🐛 Troubleshooting

### Server Won't Start

1.  Check if the path in `settings.json` is correct (must be absolute).
2.  Ensure you have installed dependencies (`pip install -r requirements.txt`).
3.  Check logs in `logs/elefante.log`.
