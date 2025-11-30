"""
Cognitive Memory Models
Defines the schema for deep cognitive analysis of memories.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class CognitiveIntent(str, Enum):
    """The user's intent behind the memory"""
    TEACHING = "teaching"       # Explaining a concept
    VENTING = "venting"         # Expressing emotion/frustration
    PLANNING = "planning"       # Outlining future actions
    REFLECTING = "reflecting"   # Analyzing past events
    DECIDING = "deciding"       # Making a choice
    QUERYING = "querying"       # Asking a question
    STATEMENT = "statement"     # Simple fact statement

class EmotionalContext(BaseModel):
    """The emotional state extracted from the memory"""
    valence: float = Field(..., description="Positive (1.0) to Negative (-1.0)")
    arousal: float = Field(..., description="Calm (0.0) to Intense (1.0)")
    mood: str = Field(..., description="Descriptive mood keyword (e.g., Frustrated, Excited)")

class ExtractedEntity(BaseModel):
    """An entity extracted from the memory"""
    name: str = Field(..., description="Name of the entity")
    type: str = Field(..., description="Type of the entity (Person, Technology, Concept, etc.)")
    description: Optional[str] = Field(None, description="Brief description or context")

class ExtractedRelationship(BaseModel):
    """A relationship between two entities"""
    source: str = Field(..., description="Name of the source entity")
    target: str = Field(..., description="Name of the target entity")
    type: str = Field(..., description="Relationship type (e.g., LOVES, BLOCKS, DEPENDS_ON)")
    reason: Optional[str] = Field(None, description="Context or reason for the relationship")

class CognitiveAnalysis(BaseModel):
    """Deep analysis of a memory's cognitive structure"""
    title: str = Field(..., description="Concise, semantic title for the memory")
    summary: str = Field(..., description="Brief summary of the memory's content")
    intent: CognitiveIntent = Field(..., description="The user's primary intent")
    emotional_context: EmotionalContext = Field(..., description="Emotional dimensions")
    entities: List[ExtractedEntity] = Field(default_factory=list, description="Entities involved")
    relationships: List[ExtractedRelationship] = Field(default_factory=list, description="Relationships between entities")
    strategic_insight: Optional[str] = Field(None, description="Actionable takeaway or rule derived from this memory")
    action: str = Field("ADD", description="ADD, UPDATE, or IGNORE")
