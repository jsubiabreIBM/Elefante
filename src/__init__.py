"""
Elefante - Local AI Memory System

A dual-database memory system combining semantic search (ChromaDB)
with structured knowledge graphs (Kuzu) for comprehensive AI memory.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from src.core.orchestrator import MemoryOrchestrator
from src.models.memory import Memory, MemoryType
from src.models.entity import Entity, Relationship

__all__ = [
    "MemoryOrchestrator",
    "Memory",
    "MemoryType",
    "Entity",
    "Relationship",
]

# Made with Bob
