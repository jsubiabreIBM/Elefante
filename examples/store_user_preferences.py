"""
Store critical user preferences in Elefante
This ensures the AI assistant remembers important working style preferences
"""

import asyncio
import sys
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.orchestrator import get_orchestrator
from src.models.memory import MemoryType

async def store_preferences():
    """Store Jaime's critical working preferences"""
    
    orchestrator = get_orchestrator()
    
    print("\n" + "="*70)
    print("🐘 STORING USER PREFERENCES IN ELEFANTE")
    print("="*70 + "\n")
    
    # Critical preference about clean environment
    print("📝 Storing CRITICAL preference: Clean environment...")
    memory1 = await orchestrator.add_memory(
        content=(
            "CRITICAL: Jaime is extremely picky about keeping the development environment clean. "
            "He HATES leftover files, test artifacts, and garbage that makes the environment "
            "hard to understand and prone to errors. The AI must avoid creating unnecessary files "
            "and always clean up after testing. This is MANDATORY and a key factor for successful development."
        ),
        memory_type=MemoryType.NOTE,
        importance=10,  # Maximum importance
        tags=["CRITICAL", "environment", "cleanliness", "development-style", "best-practices"],
        entities=[
            {"name": "Jaime Subiabre Cisterna", "type": "person"},
            {"name": "development environment", "type": "concept"},
            {"name": "clean code", "type": "concept"}
        ]
    )
    print(f"✅ Stored: {memory1.id}\n")
    
    # Additional context about working style
    print("📝 Storing working philosophy...")
    memory2 = await orchestrator.add_memory(
        content=(
            "Jaime's development philosophy: Keep the codebase clean and organized. "
            "Remove test files after validation. Avoid cluttering the workspace with "
            "temporary files. The AI should proactively suggest cleanup and maintain "
            "a pristine working environment."
        ),
        memory_type=MemoryType.NOTE,
        importance=9,
        tags=["philosophy", "organization", "cleanup", "workspace"],
        entities=[
            {"name": "Jaime Subiabre Cisterna", "type": "person"},
            {"name": "clean code", "type": "concept"}
        ]
    )
    print(f"✅ Stored: {memory2.id}\n")
    
    # Best practices reminder
    print("📝 Storing collaboration best practices...")
    memory3 = await orchestrator.add_memory(
        content=(
            "When working with Jaime: Always ask before creating test files. "
            "Clean up immediately after testing. Suggest removing unnecessary files. "
            "Keep the project structure minimal and organized. This prevents confusion "
            "and maintains code quality."
        ),
        memory_type=MemoryType.FACT,
        importance=9,
        tags=["best-practices", "workflow", "collaboration"],
        entities=[
            {"name": "Jaime Subiabre Cisterna", "type": "person"},
            {"name": "AI assistant", "type": "concept"}
        ]
    )
    print(f"✅ Stored: {memory3.id}\n")
    
    print("="*70)
    print("✅ ALL PREFERENCES STORED SUCCESSFULLY")
    print("="*70)
    print("\nThese preferences will now be automatically retrieved")
    print("whenever Bob (AI assistant) works with you!")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(store_preferences())

# Made with Bob
