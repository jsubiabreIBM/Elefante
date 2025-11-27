"""
Memory data models for Elefante
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """Types of memories that can be stored"""
    CONVERSATION = "conversation"
    FACT = "fact"
    INSIGHT = "insight"
    CODE = "code"
    DECISION = "decision"
    TASK = "task"
    NOTE = "note"
    PREFERENCE = "preference"


class MemoryStatus(str, Enum):
    """Status of a memory relative to existing knowledge"""
    NEW = "new"
    REDUNDANT = "redundant"
    CONTRADICTORY = "contradictory"
    RELATED = "related"
    CONSOLIDATED = "consolidated" # Has been merged into an insight
    REFINED = "refined" # Manually or automatically curated


class MemoryMetadata(BaseModel):
    """Metadata associated with a memory"""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    memory_type: MemoryType = MemoryType.CONVERSATION
    status: MemoryStatus = MemoryStatus.NEW
    importance: int = Field(default=5, ge=1, le=10)
    tags: List[str] = Field(default_factory=list)
    source: str = "user"  # user, agent, system
    session_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None  # For threaded memories
    
    # Additional context
    project: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    
    # Custom metadata
    custom: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }


class Memory(BaseModel):
    """Core memory object"""
    id: UUID = Field(default_factory=uuid4)
    content: str = Field(..., min_length=1)
    metadata: MemoryMetadata = Field(default_factory=MemoryMetadata)
    
    # Vector representation (populated by embedding service)
    embedding: Optional[List[float]] = None
    
    # Graph relationships (entity IDs this memory relates to)
    related_entities: List[UUID] = Field(default_factory=list)
    
    # Retrieval metadata (populated during search)
    similarity_score: Optional[float] = None
    relevance_score: Optional[float] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary"""
        return {
            "id": str(self.id),
            "content": self.content,
            "metadata": self.metadata.dict(),
            "embedding": self.embedding,
            "related_entities": [str(e) for e in self.related_entities],
            "similarity_score": self.similarity_score,
            "relevance_score": self.relevance_score,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Memory":
        """Create memory from dictionary"""
        if "id" in data and isinstance(data["id"], str):
            data["id"] = UUID(data["id"])
        if "related_entities" in data:
            data["related_entities"] = [
                UUID(e) if isinstance(e, str) else e 
                for e in data["related_entities"]
            ]
        if "metadata" in data and isinstance(data["metadata"], dict):
            data["metadata"] = MemoryMetadata(**data["metadata"])
        return cls(**data)
    
    def __str__(self) -> str:
        return f"Memory(id={self.id}, type={self.metadata.memory_type}, content='{self.content[:50]}...')"
    
    def __repr__(self) -> str:
        return self.__str__()

# Made with Bob
