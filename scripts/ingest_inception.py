import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.orchestrator import get_orchestrator
from src.utils.logger import get_logger

logger = get_logger("inception")

INCEPTION_CONTENT = """# Elefante Agentic Optimization Protocol (Inception)

## CORE IDENTITY
You are an Intelligent Agent attached to the Elefante "Second Brain". You are NOT a chatbot. You are a Cognitive Processor.

## PRIME DIRECTIVE: MEMORY FIRST
1. **Check Context**: Before answering, ALWAYS search memory (`searchMemories`).
2. **No Hallucination**: If you don't know, use `getContext` to find out.
3. **Authoritative Storage**: You define the `layer` (SELF/WORLD/INTENT).

## TOOL PROTOCOLS
- **addMemory**: Classify immediately. Detect duplications.
- **searchMemories**: Rewrite queries to be noun-centric (No pronouns).
- **queryGraph**: Use for explicit relationship tracing.

## SYSTEM STATUS
- This memory marks the successful initialization of your Cognitive Memory.
"""

async def ingest_inception():
    """
    Ingests the Inception Memory directly via Orchestrator.
    This bypasses MCP tool calls but uses the same core logic.
    """
    logger.info("🚀 Initiating Inception Protocol...")
    
    try:
        orchestrator = get_orchestrator()
        
        # Check if already exists (idempotency)
        # We search specifically for the title/concept
        existing = await orchestrator.search_memories(query="Elefante Agentic Optimization Protocol", limit=1)
        if existing and existing[0].score > 0.9: # High similarity trigger
             logger.info("✅ Inception Memory already exists. Verification passed.")
             return True

        # Ingest
        memory = await orchestrator.add_memory(
            content=INCEPTION_CONTENT,
            memory_type="insight",
            importance=10,
            metadata={
                "layer": "world",
                "sublayer": "method",
                "domain": "system", 
                "category": "protocol",
                "status": "active"
            },
            tags=["inception", "protocol", "core-directive"]
        )
        
        if memory:
            logger.info(f"✅ Inception Memory Ingested Successfully! ID: {memory.id}")
            logger.info("🧠 The Prime Directive is now active.")
            return True
        else:
            logger.error("❌ Inception Memory failed to store (returned None).")
            return False
            
    except Exception as e:
        logger.error(f"❌ Inception Failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(ingest_inception())
    if not success:
        sys.exit(1)
    sys.exit(0)
