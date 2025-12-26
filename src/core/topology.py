"""
V5 Knowledge Topology Classifier

Deterministic classification of memories into:
- ring: core | domain | topic | leaf
- knowledge_type: principle | law | preference | method | fact | decision | insight
- topic: coding-standards | communication | workflow | agent-behavior | tools-environment | collaboration | general
- summary: one-line essence
- owner_id: always "owner-jay"
"""

import re
from collections import defaultdict
from typing import Dict, Any, Tuple

# Owner constant
OWNER_ID = "owner-jay"

# Pattern matching for knowledge types
KNOWLEDGE_TYPE_PATTERNS = {
    "law": [
        r"\bLAW\s*\d+",
        r"\bNEVER\b.*\b(use|do|allow|say)\b",
        r"\bALWAYS\b.*\bMUST\b",
        r"\bMANDATORY\b",
        r"\bCRITICAL CONSTRAINT\b",
        r"\bDO NOT\b",
        r"\bFORBIDDEN\b",
        r"\bPROHIBITED\b",
    ],
    "principle": [
        r"\bThe Rule:\b",
        r"\bPRIME DIRECTIVE\b",
        r"\bCORE IDENTITY\b",
        r"\bFOUNDATION\b",
        r"\bAmbiguity is a bug\b",
        r"\bContext First\b",
        r"\bTruth\b.*\bNon-Fabrication\b",
    ],
    "method": [
        r"\bProtocol\b",
        r"\bWorkflow\b",
        r"\bPhase\s*\d+\b",
        r"\bMeta-loop\b",
        r"\bChecklist\b",
        r"→.*→",
        r"\bRequirements.*Design.*Tasks\b",
    ],
    "decision": [
        r"\bChose\b",
        r"\bDecided\b",
        r"\bWe will\b",
        r"\bSelected\b",
        r"\bprefers?\b.*\bover\b",
    ],
    "insight": [
        r"\bLearned\b",
        r"\bRealized\b",
        r"\bKey takeaway\b",
        r"\bWisdom\b",
        r"\bInception\b",
    ],
}

TOPIC_KEYWORDS = {
    "coding-standards": ["code", "comment", "formatting", "linter", "black", "test", "security", "sanitize", "emoji"],
    "communication": ["explain", "concise", "simple", "jargon", "claim", "success", "verification", "ask", "token", "brevity"],
    "workflow": ["protocol", "phase", "requirements", "design", "tasks", "implement", "verify", "kiro", "spec"],
    "agent-behavior": ["agent", "context", "memory", "search", "hallucination", "fabrication", "tool"],
    "tools-environment": ["python", "vscode", "ide", "chromadb", "kuzu", "elefante", "mcp"],
    "collaboration": ["review", "documentation", "bus factor", "team", "constructive"],
}


def infer_knowledge_type(content: str, title: str = "", memory_type: str = "", layer: str = "") -> str:
    """Infer knowledge_type from content patterns."""
    text = (content + " " + title).upper()
    
    # Check existing type as hint
    if memory_type.lower() == "decision":
        return "decision"
    if memory_type.lower() == "insight":
        return "insight"
    
    # Pattern matching
    scores = defaultdict(int)
    for ktype, patterns in KNOWLEDGE_TYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                scores[ktype] += 1
    
    if scores:
        return max(scores, key=scores.get)
    
    # Fallback based on layer
    if "constraint" in layer:
        return "law"
    if "rule" in layer:
        return "preference"
    if "method" in layer:
        return "method"
    if "fact" in layer:
        return "fact"
    if "identity" in layer:
        return "principle"
    if "preference" in layer:
        return "preference"
    
    return "fact"


def infer_topic(content: str, title: str = "", tags: str = "") -> str:
    """Infer topic from content and tags."""
    text = (content + " " + title + " " + tags).lower()
    
    scores = defaultdict(int)
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[topic] += 1
    
    if scores:
        return max(scores, key=scores.get)
    
    return "general"


def infer_ring(content: str, title: str, knowledge_type: str, importance: int, layer: str) -> str:
    """Infer ring (core/domain/topic/leaf) from attributes."""
    text = content + title
    
    # Core: Foundational principles and top laws
    if knowledge_type == "principle":
        return "core"
    if "LAW 1" in text or "LAW 0" in text:
        return "core"
    if importance >= 10 and knowledge_type == "law":
        if any(x in text for x in ["Context First", "Truth", "Non-Fabrication", "ETIQUETTE"]):
            return "core"
    
    # Domain: Self-preferences
    if layer.startswith("self/preference"):
        return "domain"
    
    # Topic: Laws and methods with high importance
    if knowledge_type in ("law", "method") and importance >= 9:
        return "topic"
    
    return "leaf"


def generate_summary(content: str, title: str) -> str:
    """Generate a one-line summary for dashboard display."""
    # If content starts with a clear statement, use first sentence
    first_line = content.split("\n")[0].strip()
    if 10 < len(first_line) < 150:
        # Remove markdown headers
        if first_line.startswith("#"):
            first_line = re.sub(r"^#+\s*", "", first_line)
        return first_line
    
    # Clean up title
    summary = re.sub(r"^(Rule|Self|Memory|E2E|Elefante)-", "", title)
    summary = re.sub(r"-", " ", summary)
    return summary.strip()[:150]


def classify_topology(
    content: str,
    title: str = "",
    memory_type: str = "",
    layer: str = "",
    sublayer: str = "",
    importance: int = 5,
    tags: str = ""
) -> Dict[str, Any]:
    """
    Full V5 topology classification.
    
    Returns dict with: ring, knowledge_type, topic, summary, owner_id
    """
    knowledge_type = infer_knowledge_type(content, title, memory_type, f"{layer}/{sublayer}")
    topic = infer_topic(content, title, tags)
    ring = infer_ring(content, title, knowledge_type, importance, f"{layer}/{sublayer}")
    summary = generate_summary(content, title)
    
    return {
        "ring": ring,
        "knowledge_type": knowledge_type,
        "topic": topic,
        "summary": summary,
        "owner_id": OWNER_ID,
    }
