# 🐘 Elefante Tutorial - Real Examples

## How to Use Your New Memory System

This guide assumes you have already installed Elefante using the **One-Click Installer**.

---

## ✅ Step 1: Verify Installation

Before starting, ensure your system is healthy:

```bash
python scripts/health_check.py
```

**Expected output:**

```
✓ Configuration: HEALTHY
✓ Embedding Service: HEALTHY
✓ Vector Store: HEALTHY
✓ Graph Store: HEALTHY
✓ Orchestrator: HEALTHY
```

---

## 🎯 Step 2: Using Elefante with Your AI Assistant

The best way to use Elefante is through your IDE (VS Code, Cursor, Claude Desktop).

### Scenario 1: Teaching Your AI About You

**You:**

> "Remember that I am a Senior Python Developer at IBM. I specialize in building AI agents using Autogen and LangChain."

**AI (using `addMemory`):**

> "I've stored that information. I've linked 'IBM', 'Autogen', and 'LangChain' to your profile."

**You:**

> "What do you know about my tech stack?"

**AI (using `searchMemories`):**

> "You specialize in Python, Autogen, and LangChain."

---

### Scenario 2: Project Context

**You:**

> "I'm starting a new project called 'Project Omega'. It's a distributed system using Kafka and Redis."

**AI (using `addMemory`):**

> "Noted. I've created a new entity for 'Project Omega' and linked 'Kafka' and 'Redis' to it."

**You:**

> "What technologies does Project Omega use?"

**AI (using `queryGraph`):**

> "Project Omega uses Kafka and Redis."

---

## 💻 Step 3: Python API Examples

You can also use Elefante programmatically in your own scripts.

### Example 1: Store & Search

Create `examples/demo_basic.py`:

```python
import asyncio
from src.core.orchestrator import get_orchestrator

async def main():
    orch = get_orchestrator()

    # 1. Add Memory
    print("Storing memory...")
    await orch.add_memory(
        content="Elefante uses a triple-layer architecture: Vector, Graph, and Context.",
        memory_type="fact",
        tags=["architecture", "elefante"]
    )

    # 2. Search
    print("\nSearching...")
    results = await orch.search_memories("How is Elefante designed?")

    for r in results:
        print(f"- {r.memory.content} (Score: {r.score:.2f})")

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 2: Knowledge Graph

Create `examples/demo_graph.py`:

```python
import asyncio
from src.core.orchestrator import get_orchestrator

async def main():
    orch = get_orchestrator()

    # Create entities manually
    print("Creating graph...")
    user = await orch.create_entity(name="Jaime", type="person")
    project = await orch.create_entity(name="Elefante", type="project")

    # Link them
    await orch.create_relationship(
        from_entity_id=user.id,
        to_entity_id=project.id,
        relationship_type="created"
    )

    print("Relationship created: Jaime -> created -> Elefante")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🔍 Step 4: Exploring Your Data

You can inspect your databases directly if needed.

**Vector Store (ChromaDB):**
Located in `data/chroma/`. Contains embeddings and text.

**Graph Store (Kuzu):**
Located in `data/kuzu/`. Contains nodes and edges.

To reset everything and start fresh:

```bash
# WARNING: Deletes all memories!
rm -rf data/
python scripts/init_databases.py
```
