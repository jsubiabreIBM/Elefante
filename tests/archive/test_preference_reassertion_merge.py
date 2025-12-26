import pytest
from uuid import uuid4

from src.core.orchestrator import MemoryOrchestrator
from src.core.vector_store import VectorStore
from src.core.graph_store import GraphStore
from src.models.memory import MemoryType


@pytest.fixture
def isolated_orchestrator(tmp_path):
    chroma_dir = tmp_path / "chroma"
    kuzu_dir = tmp_path / "kuzu_db"

    vector_store = VectorStore(
        collection_name=f"test_pref_merge_{uuid4().hex}",
        persist_directory=str(chroma_dir),
    )
    graph_store = GraphStore(database_path=str(kuzu_dir))

    return MemoryOrchestrator(vector_store=vector_store, graph_store=graph_store)


@pytest.mark.asyncio
async def test_preference_reassertion_merges_instead_of_creating_new(isolated_orchestrator):
    m1 = await isolated_orchestrator.add_memory(
        content="Agents should communicate in simple terms and be concise.",
        memory_type=MemoryType.PREFERENCE.value,
        importance=8,
        tags=["preference", "communication", "simple", "concise"],
        metadata={"layer": "self", "sublayer": "constraint", "category": "communication"},
    )
    assert m1 is not None

    stats_1 = await isolated_orchestrator.vector_store.get_stats()
    assert stats_1.get("total_memories") == 1

    m2 = await isolated_orchestrator.add_memory(
        content="Always communicate concisely in simple terms; no fluff.",
        memory_type=MemoryType.PREFERENCE.value,
        importance=9,
        tags=["communication-style", "brevity"],
        metadata={"layer": "self", "sublayer": "preference", "category": "communication"},
    )
    assert m2 is not None

    # Must return the existing memory instead of creating a new one.
    assert m2.id == m1.id

    stats_2 = await isolated_orchestrator.vector_store.get_stats()
    assert stats_2.get("total_memories") == 1

    refreshed = await isolated_orchestrator.vector_store.get_memory(m1.id)
    assert refreshed is not None
    assert refreshed.metadata.access_count >= 2
    assert refreshed.metadata.importance >= 9

    # Tags should merge (existing + new).
    all_tags = set(refreshed.metadata.tags or [])
    assert "communication" in all_tags
    assert "brevity" in all_tags

    # Content should retain the core preference.
    assert "simple" in refreshed.content.lower()
    assert "concise" in refreshed.content.lower()
