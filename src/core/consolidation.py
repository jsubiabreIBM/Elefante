"""
Memory Consolidation Module
Handles the synthesis of recent memories into higher-level insights using LLMs.
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from uuid import uuid4, UUID

from src.models.memory import Memory, MemoryType, MemoryStatus
from src.models.entity import EntityType, RelationshipType
from src.core.vector_store import get_vector_store
from src.core.graph_store import get_graph_store
from src.core.llm import get_llm_service
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MemoryConsolidator:
    """
    Consolidates raw memories into refined insights.
    """
    
    def __init__(self):
        self.vector_store = get_vector_store()
        self.graph_store = get_graph_store()
        self.llm_service = get_llm_service()
        self.logger = get_logger(self.__class__.__name__)
        
    async def consolidate_recent(self, hours: int = 24, force: bool = False) -> List[Memory]:
        """
        Analyze memories from the last N hours and consolidate them.
        """
        self.logger.info(f"Starting memory consolidation (last {hours}h)")
        
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

        # 2. Prepare context for LLM
        memory_text = "\n\n".join([
            f"ID: {m['id']}\nTime: {m['timestamp']}\nContent: {m['content']}" 
            for m in memories_to_process
        ])
        
        system_prompt = """
        You are an expert memory analyst. Analyze the provided list of recent user memories/interactions.
        Identify key themes, decisions, facts, and patterns.
        Synthesize them into a set of concise "Insights" or "Facts".
        Ignore trivial chit-chat. Focus on long-term value.
        
        Return a JSON object with a list of "insights":
        {
            "insights": [
                {
                    "content": "The user prefers Python for backend development.",
                    "type": "fact",
                    "source_memory_ids": ["id1", "id2"]
                },
                {
                    "content": "Project Elefante is a local-first memory system using Kuzu and ChromaDB.",
                    "type": "insight",
                    "source_memory_ids": ["id3"]
                }
            ]
        }
        """
        
        # 3. Call LLM
        self.logger.info(f"Sending {len(memories_to_process)} memories to LLM for analysis")
        response = await self.llm_service.generate_response(system_prompt, memory_text)
        
        try:
            # Parse JSON (handle potential markdown blocks)
            cleaned_response = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned_response)
            insights = data.get("insights", [])
        except Exception as e:
            self.logger.error(f"Failed to parse LLM response: {e}\nResponse: {response}")
            return []
            
        new_memories = []
        
        # 4. Store new insights
        from src.core.orchestrator import get_orchestrator
        orchestrator = get_orchestrator() # Use orchestrator to add new memories properly
        
        for insight in insights:
            content = insight.get("content")
            m_type = insight.get("type", "insight")
            source_ids = insight.get("source_memory_ids", [])
            
            if not content:
                continue
                
            self.logger.info(f"Created new insight: {content[:50]}...")
            
            # Add the new memory
            new_memory = await orchestrator.add_memory(
                content=content,
                memory_type=m_type,
                importance=8, # High importance for consolidated insights
                tags=["consolidated", "auto-generated"],
                metadata={"source_memory_ids": source_ids}
            )
            new_memories.append(new_memory)
            
            # Link back to source memories (CONSOLIDATED_FROM)
            # We need to manually create these relationships as add_memory doesn't handle ID linking
            for source_id in source_ids:
                try:
                    # Mark source as consolidated (optional, maybe just link them)
                    # For now, we just link them
                    await orchestrator.create_relationship(
                        from_entity_id=new_memory.id,
                        to_entity_id=UUID(source_id) if isinstance(source_id, str) else source_id,
                        relationship_type="consolidated_from" # Custom type
                    )
                    
                    # Mark source as consolidated in Graph
                    update_cypher = f"""
                    MATCH (m:Entity {{id: '{source_id}'}})
                    SET m.status = 'consolidated'
                    RETURN m
                    """
                    await self.graph_store.execute_query(update_cypher)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to link/update source {source_id}: {e}")
                    
        return new_memories

import json
