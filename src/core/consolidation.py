"""
Memory Consolidation Module
Handles the synthesis of recent memories into higher-level insights.

ARCHITECTURE RULE:
Elefante must not call LLMs directly. Consolidation is therefore agent-driven:
an external agent can fetch recent memories, run any LLM it wants, then call
Elefante tools to store the consolidated insights.
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from uuid import uuid4, UUID

from src.models.memory import Memory, MemoryType, MemoryStatus
from src.models.entity import EntityType, RelationshipType
from src.core.vector_store import get_vector_store
from src.core.graph_store import get_graph_store
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MemoryConsolidator:
    """
    Consolidates raw memories into refined insights.
    """
    
    def __init__(self):
        self.vector_store = get_vector_store()
        self.graph_store = get_graph_store()
        self.logger = get_logger(self.__class__.__name__)
        
    async def consolidate_recent(self, hours: int = 24, force: bool = False) -> List[Memory]:
        """
        Analyze memories from the last N hours and consolidate them.
        """
        self.logger.info(f"Starting memory consolidation (last {hours}h)")

        # Agent-driven consolidation: this built-in consolidator is intentionally disabled.
        # External callers should implement consolidation outside Elefante and then write
        # the synthesized memories via the normal add_memory pipeline.
        self.logger.warning("consolidation_disabled_agent_managed")
        return []
        
        # 1. Fetch recent memories
        # We'll use the graph store to find memories by timestamp as it's more reliable for time queries
        cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        
        cypher = f"""
        MATCH (m:Entity {{type: 'memory'}})
        WHERE m.timestamp >= '{cutoff}' AND m.status <> 'consolidated'
        RETURN m
        ORDER BY m.timestamp DESC
        LIMIT 100
        """
        
        results = await self.graph_store.execute_query(cypher)
        
        memories_to_process = []
        for row in results:
            entity = row.get("m")
            if entity:
                memories_to_process.append({
                    "id": str(entity.id),
                    "content": entity.properties.get("content", ""),
                    "timestamp": entity.properties.get("timestamp")
                })
        
        if not memories_to_process:
            self.logger.info("No recent memories to consolidate")
            return []
            
        if len(memories_to_process) < 5 and not force:
            self.logger.info(f"Not enough memories to consolidate ({len(memories_to_process)} < 5)")
            return []


