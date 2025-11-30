# 🐘 Elefante

**Local. Private. Triple-Layer AI Memory.**

Elefante is a local-first memory system designed to provide "perfect memory" for AI agents. It creates a stateful brain for your AI by combining semantic search, structured knowledge graphs, and conversation context—all running 100% on your machine.

## ⚡ Core Features

- **Triple-Layer Architecture:** Combines **ChromaDB** (Semantic), **Kuzu** (Graph), and **Session Context** for robust retrieval.
- **Privacy First:** Zero data egress. Your memories live in `./data`, not the cloud.
- **MCP Native:** Built specifically for the **Model Context Protocol**, making it plug-and-play for Cursor, Claude Desktop, and Bob IDE.
- **Adaptive Weighting:** Dynamically adjusts retrieval strategies based on query intent (e.g., questions favor semantic search, IDs favor graph lookups).

## 🚀 Quick Start

**Windows:**
Run `install.bat` to install dependencies and configure your IDE automatically.

**Mac/Linux:**
Run `./install.sh`.

For detailed instructions, see [docs/INSTALLATION.md](docs/INSTALLATION.md).

## 🧠 Usage

Simply talk to your agent:

> "Remember that I am a Senior Python Developer at IBM."
> "What is the relationship between Project Omega and Kafka?"

For API examples and advanced queries, see [docs/USAGE.md](docs/USAGE.md).

## 🏗️ Architecture

Elefante uses an **Orchestrator Pattern** to route queries:
`User -> MCP Server -> Orchestrator -> (Vector + Graph + Context) -> Weighted Result`.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the deep dive.
