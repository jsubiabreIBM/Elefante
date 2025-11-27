# Elefante Setup Guide - Fresh Installation

## For New Agents/Developers/Environments

This guide ensures zero-issue installation of Elefante from scratch.

---

## 🚀 One-Click Installation (Recommended)

The easiest way to get started is using the automated installer.

### Windows

Double-click `install.bat` in the project root.

### Mac/Linux

```bash
chmod +x install.sh
./install.sh
```

**What this does:**

1.  Creates a virtual environment (`.venv`)
2.  Installs all dependencies
3.  Initializes ChromaDB and Kuzu databases
4.  **Configures your IDE** (VSCode/Bob) automatically
5.  Runs a system health check

---

## 🛠️ Manual Installation

If you prefer to set up manually, follow these steps.

### Prerequisites

- **Python 3.10+** (verify: `python --version`)
- **Git** (verify: `git --version`)

### Step 1: Clone Repository

```bash
git clone https://github.com/jsubiabreIBM/Elefante.git
cd Elefante
```

### Step 2: Create Virtual Environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Initialize Databases

```bash
python scripts/init_databases.py
```

### Step 5: Configure IDE (MCP)

```bash
python scripts/configure_vscode_bob.py
```

### Step 6: Verify Installation

```bash
python scripts/health_check.py
```

---

## 🐛 Troubleshooting

### "ChromaDB not found"

```bash
pip install chromadb
```

### "Kuzu import error"

```bash
pip install kuzu
```

### "Embedding model download failed"

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### "Database initialization failed"

```bash
# Reset databases (WARNING: Deletes all memories)
rm -rf data/
python scripts/init_databases.py
```

---

## Support

**Issues?**

1. Check the logs in `logs/`
2. Run `python scripts/health_check.py`
3. Open a GitHub Issue with your error message.
