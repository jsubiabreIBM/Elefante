"""
Vector store implementation using ChromaDB

Provides semantic memory storage and retrieval using vector embeddings.
"""

import asyncio
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pathlib import Path

from src.models.memory import Memory, MemoryMetadata
from src.models.query import SearchResult, SearchFilters
from src.core.embeddings import get_embedding_service
from src.utils.config import get_config
from src.utils.logger import get_logger
from src.utils.validators import validate_memory_content, validate_limit

logger = get_logger(__name__)


class VectorStore:
    """
    Vector store for semantic memory using ChromaDB
    
    Stores memories with their vector embeddings and provides
    similarity-based search capabilities.
    """
    
    def __init__(self, collection_name: Optional[str] = None, persist_directory: Optional[str] = None):
        """
        Initialize vector store
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory for persistent storage
        """
        self.config = get_config()
        self.collection_name = collection_name or self.config.elefante.vector_store.collection_name
        self.persist_directory = persist_directory or self.config.elefante.vector_store.persist_directory
        self.distance_metric = self.config.elefante.vector_store.distance_metric
        
        self._client = None
        self._collection = None
        self._embedding_service = get_embedding_service()
        
        logger.info(
            "initializing_vector_store",
            collection=self.collection_name,
            persist_dir=self.persist_directory
        )
    
    def _initialize_client(self):
        """Initialize ChromaDB client (lazy loading)"""
        if self._client is not None:
            return
        
        try:
            import chromadb
            from chromadb.config import Settings
            
            # Create persist directory if it doesn't exist
            Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
            
            # Initialize client with persistent storage
            self._client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self._collection = self._client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": self.distance_metric}
            )
            
            logger.info(
                "chromadb_initialized",
                collection=self.collection_name,
                count=self._collection.count()
            )
            
        except ImportError:
            logger.error("chromadb_not_installed")
            raise ImportError(
                "chromadb not installed. "
                "Install with: pip install chromadb"
            )
        except Exception as e:
            logger.error("failed_to_initialize_chromadb", error=str(e))
            raise
    
    async def add_memory(self, memory: Memory) -> str:
        """
        Add a memory to the vector store
        
        Args:
            memory: Memory object to store
            
        Returns:
            Memory ID as string
        """
        self._initialize_client()
        
        # Validate content
        validate_memory_content(memory.content)
        
        # Generate embedding if not provided
        if memory.embedding is None:
            logger.debug("generating_embedding", memory_id=str(memory.id))
            memory.embedding = await self._embedding_service.generate_embedding(memory.content)
        
        # Prepare metadata for ChromaDB
        metadata = {
            "timestamp": memory.metadata.timestamp.isoformat(),
            "memory_type": memory.metadata.memory_type.value,
            "importance": memory.metadata.importance,
            "tags": ",".join(memory.metadata.tags) if memory.metadata.tags else "",
            "source": memory.metadata.source,
        }
        
        # Add optional metadata
        if memory.metadata.session_id:
            metadata["session_id"] = str(memory.metadata.session_id)
        if memory.metadata.project:
            metadata["project"] = memory.metadata.project
        if memory.metadata.file_path:
            metadata["file_path"] = memory.metadata.file_path
        
        # Add to collection
        try:
            await asyncio.to_thread(
                self._collection.add,
                ids=[str(memory.id)],
                embeddings=[memory.embedding],
                documents=[memory.content],
                metadatas=[metadata]
            )
            
            logger.info(
                "memory_added",
                memory_id=str(memory.id),
                type=memory.metadata.memory_type.value
            )
            
            return str(memory.id)
            
        except Exception as e:
            logger.error("failed_to_add_memory", memory_id=str(memory.id), error=str(e))
            raise
    
    async def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[SearchFilters] = None,
        min_similarity: Optional[float] = None
    ) -> List[SearchResult]:
        """
        Search for similar memories
        
        Args:
            query: Search query text
            limit: Maximum number of results
            filters: Optional filters to apply
            min_similarity: Minimum similarity threshold (0-1)
            
        Returns:
            List of search results with scores
        """
        self._initialize_client()
        
        # Validate inputs
        limit = validate_limit(limit)
        min_similarity = min_similarity or self.config.elefante.orchestrator.min_similarity
        
        # Generate query embedding
        logger.debug("searching_memories", query=query[:50], limit=limit)
        query_embedding = await self._embedding_service.generate_embedding(query)
        
        # Build where clause from filters
        where_clause = self._build_where_clause(filters) if filters else None
        
        # Perform search
        try:
            results = await asyncio.to_thread(
                self._collection.query,
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
            
            # Convert to SearchResult objects
            search_results = []
            
            if results and results['ids'] and len(results['ids'][0]) > 0:
                for i in range(len(results['ids'][0])):
                    memory_id = results['ids'][0][i]
                    content = results['documents'][0][i]
                    metadata_dict = results['metadatas'][0][i]
                    distance = results['distances'][0][i]
                    
                    # Convert distance to similarity score (0-1)
                    # For cosine distance: similarity = 1 - distance
                    similarity = 1.0 - distance
                    
                    # Clamp similarity to [0.0, 1.0] to handle floating-point precision issues
                    similarity = max(0.0, min(1.0, similarity))
                    
                    # Filter by minimum similarity
                    if similarity < min_similarity:
                        continue
                    
                    # Reconstruct memory object
                    memory = self._reconstruct_memory(memory_id, content, metadata_dict)
                    memory.similarity_score = similarity
                    
                    # Create search result
                    result = SearchResult(
                        memory=memory,
                        score=similarity,
                        source="vector",
                        vector_score=similarity
                    )
                    
                    search_results.append(result)
            
            logger.info(
                "search_completed",
                query=query[:50],
                results_count=len(search_results)
            )
            
            return search_results
            
        except Exception as e:
            logger.error("search_failed", query=query[:50], error=str(e))
            raise
    
    def _build_where_clause(self, filters: SearchFilters) -> Dict[str, Any]:
        """Build ChromaDB where clause from filters"""
        where = {}
        
        if filters.memory_type:
            where["memory_type"] = filters.memory_type
        
        if filters.source:
            where["source"] = filters.source
        
        if filters.project:
            where["project"] = filters.project
        
        if filters.min_importance is not None:
            where["importance"] = {"$gte": filters.min_importance}
        
        # Note: ChromaDB has limited filtering capabilities
        # Complex filters (tags, dates) may need post-processing
        
        return where if where else None
    
    def _reconstruct_memory(self, memory_id: str, content: str, metadata: Dict[str, Any]) -> Memory:
        """Reconstruct Memory object from ChromaDB data"""
        # Parse metadata
        memory_metadata = MemoryMetadata(
            timestamp=datetime.fromisoformat(metadata.get("timestamp", datetime.utcnow().isoformat())),
            memory_type=metadata.get("memory_type", "conversation"),
            importance=metadata.get("importance", 5),
            tags=metadata.get("tags", "").split(",") if metadata.get("tags") else [],
            source=metadata.get("source", "user"),
        )
        
        # Add optional fields
        if session_id := metadata.get("session_id"):
            memory_metadata.session_id = UUID(session_id)
        if project := metadata.get("project"):
            memory_metadata.project = project
        if file_path := metadata.get("file_path"):
            memory_metadata.file_path = file_path
        
        # Create memory object
        memory = Memory(
            id=UUID(memory_id),
            content=content,
            metadata=memory_metadata
        )
        
        return memory
    
    async def get_memory(self, memory_id: UUID) -> Optional[Memory]:
        """
        Get a specific memory by ID
        
        Args:
            memory_id: Memory UUID
            
        Returns:
            Memory object or None if not found
        """
        self._initialize_client()
        
        try:
            result = await asyncio.to_thread(
                self._collection.get,
                ids=[str(memory_id)],
                include=["documents", "metadatas", "embeddings"]
            )
            
            if result and result['ids'] and len(result['ids']) > 0:
                memory = self._reconstruct_memory(
                    result['ids'][0],
                    result['documents'][0],
                    result['metadatas'][0]
                )
                memory.embedding = result['embeddings'][0] if result['embeddings'] else None
                
                return memory
            
            return None
            
        except Exception as e:
            logger.error("failed_to_get_memory", memory_id=str(memory_id), error=str(e))
            return None
    
    async def update_memory(self, memory_id: UUID, updates: Dict[str, Any]) -> bool:
        """
        Update a memory's metadata or content
        
        Args:
            memory_id: Memory UUID
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        self._initialize_client()
        
        try:
            # Get existing memory
            memory = await self.get_memory(memory_id)
            if not memory:
                logger.warning("memory_not_found_for_update", memory_id=str(memory_id))
                return False
            
            # Update fields
            if "content" in updates:
                memory.content = updates["content"]
                # Regenerate embedding
                memory.embedding = await self._embedding_service.generate_embedding(memory.content)
            
            if "importance" in updates:
                memory.metadata.importance = updates["importance"]
            
            if "tags" in updates:
                memory.metadata.tags = updates["tags"]
            
            # Delete old and add updated
            await self.delete_memory(memory_id)
            await self.add_memory(memory)
            
            logger.info("memory_updated", memory_id=str(memory_id))
            return True
            
        except Exception as e:
            logger.error("failed_to_update_memory", memory_id=str(memory_id), error=str(e))
            return False
    
    async def delete_memory(self, memory_id: UUID) -> bool:
        """
        Delete a memory from the vector store
        
        Args:
            memory_id: Memory UUID
            
        Returns:
            True if successful, False otherwise
        """
        self._initialize_client()
        
        try:
            await asyncio.to_thread(
                self._collection.delete,
                ids=[str(memory_id)]
            )
            
            logger.info("memory_deleted", memory_id=str(memory_id))
            return True
            
        except Exception as e:
            logger.error("failed_to_delete_memory", memory_id=str(memory_id), error=str(e))
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get vector store statistics
        
        Returns:
            Dictionary with statistics
        """
        self._initialize_client()
        
        try:
            count = await asyncio.to_thread(self._collection.count)
            
            return {
                "collection_name": self.collection_name,
                "total_memories": count,
                "persist_directory": self.persist_directory,
                "distance_metric": self.distance_metric,
                "embedding_dimension": self._embedding_service.get_embedding_dimension()
            }
            
        except Exception as e:
            logger.error("failed_to_get_stats", error=str(e))
            return {}
    
    async def clear(self) -> bool:
        """
        Clear all memories from the vector store
        
        WARNING: This deletes all data!
        
        Returns:
            True if successful
        """
        self._initialize_client()
        
        try:
            # Delete collection and recreate
            await asyncio.to_thread(self._client.delete_collection, self.collection_name)
            self._collection = await asyncio.to_thread(
                self._client.create_collection,
                name=self.collection_name,
                metadata={"hnsw:space": self.distance_metric}
            )
            
            logger.warning("vector_store_cleared", collection=self.collection_name)
            return True
            
        except Exception as e:
            logger.error("failed_to_clear_vector_store", error=str(e))
            return False
    
    def __repr__(self) -> str:
        return f"VectorStore(collection={self.collection_name}, persist_dir={self.persist_directory})"


# Global vector store instance
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """
    Get global vector store instance
    
    Returns:
        VectorStore: Global vector store
    """
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store


def reset_vector_store():
    """Reset global vector store (useful for testing)"""
    global _vector_store
    _vector_store = None

# Made with Bob
