# Elefante Implementation Plan

**Status**: Architecture Complete - Ready for Implementation  
**Date**: 2025-11-25  
**Phase**: 1 - Core Development  

---

## 📋 Implementation Checklist

### ✅ Phase 0: Architecture & Design (COMPLETE)
- [x] Create ARCHITECTURE.md with full system design
- [x] Create README.md with user documentation
- [x] Define data models (Memory, Entity, Relationship, Query)
- [x] Design MCP tool schemas
- [x] Create configuration templates
- [x] Set up project structure

### 🚧 Phase 1: Core Infrastructure (NEXT)

#### 1.1 Configuration Management
**Files to Create:**
- [ ] `src/utils/__init__.py`
- [ ] `src/utils/config.py` - Configuration loader and validator
- [ ] `src/utils/logger.py` - Structured logging setup
- [ ] `src/utils/validators.py` - Input validation utilities

**Implementation Details:**
```python
# src/utils/config.py
- Load config.yaml with environment variable overrides
- Validate all configuration values
- Provide singleton access to config
- Support hot-reloading (optional)

# src/utils/logger.py
- Set up structlog with JSON formatting
- Configure file rotation
- Add context managers for request tracing
```

#### 1.2 Embedding Service
**Files to Create:**
- [ ] `src/core/__init__.py`
- [ ] `src/core/embeddings.py` - Embedding generation service

**Implementation Details:**
```python
# src/core/embeddings.py
class EmbeddingService:
    - Initialize sentence-transformers model
    - Batch embedding generation
    - Caching mechanism
    - Fallback to OpenAI (optional)
    - Async support with asyncio
    
Methods:
    - async def generate_embedding(text: str) -> List[float]
    - async def generate_embeddings_batch(texts: List[str]) -> List[List[float]]
    - def get_embedding_dimension() -> int
```

**Dependencies:**
- sentence-transformers
- torch (CPU version)
- numpy

#### 1.3 Vector Store (ChromaDB)
**Files to Create:**
- [ ] `src/core/vector_store.py` - ChromaDB wrapper

**Implementation Details:**
```python
# src/core/vector_store.py
class VectorStore:
    - Initialize ChromaDB with persistent storage
    - Create/get collection
    - CRUD operations for memories
    - Similarity search with filters
    - Metadata filtering
    
Methods:
    - async def add_memory(memory: Memory) -> str
    - async def search(query: str, limit: int, filters: dict) -> List[SearchResult]
    - async def get_memory(memory_id: UUID) -> Optional[Memory]
    - async def update_memory(memory_id: UUID, updates: dict) -> bool
    - async def delete_memory(memory_id: UUID) -> bool
    - async def get_stats() -> dict
```

**Key Features:**
- Automatic embedding generation via EmbeddingService
- Metadata filtering (type, importance, tags, dates)
- Cosine similarity search
- Batch operations for efficiency

#### 1.4 Graph Store (Kuzu)
**Files to Create:**
- [ ] `src/core/graph_store.py` - Kuzu wrapper

**Implementation Details:**
```python
# src/core/graph_store.py
class GraphStore:
    - Initialize Kuzu database
    - Create schema (node types, relationship types)
    - CRUD operations for entities and relationships
    - Cypher-like query execution
    - Graph traversal operations
    
Methods:
    # Entity operations
    - async def create_entity(entity: Entity) -> UUID
    - async def get_entity(entity_id: UUID) -> Optional[Entity]
    - async def update_entity(entity_id: UUID, updates: dict) -> bool
    - async def delete_entity(entity_id: UUID) -> bool
    
    # Relationship operations
    - async def create_relationship(rel: Relationship) -> UUID
    - async def get_relationships(entity_id: UUID) -> List[Relationship]
    - async def delete_relationship(rel_id: UUID) -> bool
    
    # Query operations
    - async def execute_query(cypher: str, params: dict) -> List[dict]
    - async def find_path(from_id: UUID, to_id: UUID, max_depth: int) -> List[dict]
    - async def get_neighbors(entity_id: UUID, depth: int) -> List[Entity]
```

**Schema Setup:**
```cypher
// Node types
CREATE NODE TABLE Memory(id STRING, content STRING, timestamp TIMESTAMP, type STRING, importance INT, PRIMARY KEY(id))
CREATE NODE TABLE Entity(id STRING, name STRING, type STRING, description STRING, PRIMARY KEY(id))
CREATE NODE TABLE Session(id STRING, start_time TIMESTAMP, end_time TIMESTAMP, PRIMARY KEY(id))

// Relationship types
CREATE REL TABLE RELATES_TO(FROM Memory TO Entity, strength DOUBLE)
CREATE REL TABLE PART_OF(FROM Memory TO Session)
CREATE REL TABLE DEPENDS_ON(FROM Entity TO Entity, description STRING)
CREATE REL TABLE REFERENCES(FROM Memory TO Memory)
```

#### 1.5 Hybrid Orchestrator
**Files to Create:**
- [ ] `src/core/orchestrator.py` - Main orchestration layer

**Implementation Details:**
```python
# src/core/orchestrator.py
class MemoryOrchestrator:
    - Coordinate between VectorStore and GraphStore
    - Intelligent query routing
    - Result merging and ranking
    - Transaction management
    
Methods:
    # Memory operations
    - async def add_memory(content: str, **kwargs) -> Memory
    - async def search(query: str, mode: QueryMode, **kwargs) -> List[SearchResult]
    - async def get_context(session_id: UUID, depth: int) -> dict
    
    # Entity operations
    - async def create_entity(name: str, type: EntityType, **kwargs) -> Entity
    - async def create_relationship(from_id: UUID, to_id: UUID, rel_type: RelationshipType) -> Relationship
    
    # Query operations
    - async def query_graph(cypher: str, params: dict) -> List[dict]
    - def _analyze_query(query: str) -> QueryPlan
    - async def _merge_results(vector_results, graph_results, plan: QueryPlan) -> List[SearchResult]
```

**Query Routing Logic:**
```python
def _analyze_query(self, query: str) -> QueryPlan:
    # Semantic indicators
    if any(kw in query.lower() for kw in ["similar", "like", "about", "related"]):
        return QueryPlan(mode=QueryMode.SEMANTIC, vector_weight=0.8, graph_weight=0.2)
    
    # Structural indicators
    elif any(kw in query.lower() for kw in ["who", "what", "when", "depends", "blocks"]):
        return QueryPlan(mode=QueryMode.STRUCTURED, vector_weight=0.2, graph_weight=0.8)
    
    # Default: Hybrid
    else:
        return QueryPlan(mode=QueryMode.HYBRID, vector_weight=0.5, graph_weight=0.5)
```

---

### 🔌 Phase 2: MCP Integration

#### 2.1 MCP Server
**Files to Create:**
- [ ] `src/mcp/__init__.py`
- [ ] `src/mcp/server.py` - MCP server implementation
- [ ] `src/mcp/tools.py` - Tool definitions
- [ ] `src/mcp/handlers.py` - Tool execution handlers

**Implementation Details:**
```python
# src/mcp/server.py
class ElefanteMCPServer:
    - Initialize MCP server
    - Register tools
    - Handle tool calls
    - Error handling and logging
    
# src/mcp/tools.py
TOOLS = [
    {
        "name": "addMemory",
        "description": "Store a new memory",
        "inputSchema": {...}
    },
    {
        "name": "searchMemories",
        "description": "Search memories",
        "inputSchema": {...}
    },
    # ... other tools
]

# src/mcp/handlers.py
async def handle_add_memory(args: dict) -> dict
async def handle_search_memories(args: dict) -> dict
async def handle_query_graph(args: dict) -> dict
async def handle_create_entity(args: dict) -> dict
async def handle_create_relationship(args: dict) -> dict
async def handle_get_context(args: dict) -> dict
```

---

### 🧪 Phase 3: Testing

#### 3.1 Unit Tests
**Files to Create:**
- [ ] `tests/__init__.py`
- [ ] `tests/test_vector_store.py`
- [ ] `tests/test_graph_store.py`
- [ ] `tests/test_orchestrator.py`
- [ ] `tests/test_embeddings.py`
- [ ] `tests/test_models.py`

**Test Coverage:**
- Vector store CRUD operations
- Graph store CRUD operations
- Embedding generation
- Query routing logic
- Result merging
- Data model validation

#### 3.2 Integration Tests
**Files to Create:**
- [ ] `tests/test_integration.py`
- [ ] `tests/test_mcp_server.py`

**Test Scenarios:**
- End-to-end memory storage and retrieval
- Hybrid search accuracy
- MCP tool execution
- Database synchronization
- Error handling and recovery

#### 3.3 Performance Tests
**Files to Create:**
- [ ] `tests/test_performance.py`

**Benchmarks:**
- Memory storage latency
- Search query latency
- Concurrent query handling
- Memory usage profiling
- Scalability (1k, 10k, 100k memories)

---

### 🛠️ Phase 4: Utilities & Scripts

#### 4.1 Initialization Scripts
**Files to Create:**
- [ ] `scripts/__init__.py`
- [ ] `scripts/init_databases.py` - Initialize ChromaDB and Kuzu
- [ ] `scripts/health_check.py` - System health verification
- [ ] `scripts/migrate_data.py` - Data migration utilities

**Implementation:**
```python
# scripts/init_databases.py
- Create data directories
- Initialize ChromaDB collection
- Create Kuzu schema
- Verify connectivity
- Load sample data (optional)

# scripts/health_check.py
- Check database connectivity
- Verify embedding service
- Test basic operations
- Report system status
```

#### 4.2 CLI Interface (Optional)
**Files to Create:**
- [ ] `src/cli.py` - Command-line interface

**Commands:**
```bash
elefante init          # Initialize databases
elefante add "text"    # Add memory
elefante search "query" # Search memories
elefante stats         # Show statistics
elefante health        # Health check
```

---

### 📚 Phase 5: Documentation

#### 5.1 API Documentation
**Files to Create:**
- [ ] `docs/API.md` - Complete API reference
- [ ] `docs/EXAMPLES.md` - Usage examples
- [ ] `docs/TROUBLESHOOTING.md` - Common issues

#### 5.2 Additional Docs
**Files to Create:**
- [ ] `CONTRIBUTING.md` - Contribution guidelines
- [ ] `LICENSE` - MIT License
- [ ] `CHANGELOG.md` - Version history

---

## 🎯 Implementation Priority

### Critical Path (Must Have for MVP)
1. ✅ Configuration management (`src/utils/config.py`)
2. ✅ Embedding service (`src/core/embeddings.py`)
3. ✅ Vector store (`src/core/vector_store.py`)
4. ✅ Graph store (`src/core/graph_store.py`)
5. ✅ Orchestrator (`src/core/orchestrator.py`)
6. ✅ MCP server (`src/mcp/server.py`)
7. ✅ Initialization script (`scripts/init_databases.py`)
8. ✅ Basic tests

### Important (Should Have)
- Health check script
- Comprehensive test suite
- API documentation
- Error handling improvements

### Nice to Have (Could Have)
- CLI interface
- Performance optimizations
- Advanced graph algorithms
- Web UI (future)

---

## 🔧 Development Guidelines

### Code Style
- Use Black for formatting
- Type hints for all functions
- Docstrings (Google style)
- Async/await for I/O operations

### Error Handling
- Use custom exceptions
- Graceful degradation
- Comprehensive logging
- User-friendly error messages

### Testing
- Minimum 80% code coverage
- Test edge cases
- Mock external dependencies
- Use pytest fixtures

### Performance
- Batch operations where possible
- Cache embeddings
- Use connection pooling
- Profile critical paths

---

## 📦 Dependencies to Install

```bash
# Core
pip install chromadb kuzu sentence-transformers

# MCP
pip install mcp

# Utilities
pip install pyyaml python-dotenv structlog aiohttp numpy pydantic

# Development
pip install pytest pytest-asyncio pytest-cov black mypy
```

---

## 🚀 Getting Started with Implementation

### Step 1: Set Up Environment
```bash
cd Elefante
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Step 2: Implement Core Components (in order)
1. Start with `src/utils/config.py`
2. Then `src/core/embeddings.py`
3. Then `src/core/vector_store.py`
4. Then `src/core/graph_store.py`
5. Then `src/core/orchestrator.py`
6. Finally `src/mcp/server.py`

### Step 3: Test Each Component
- Write tests as you implement
- Run `pytest tests/` frequently
- Verify with `scripts/health_check.py`

### Step 4: Integration
- Connect all components
- Test end-to-end workflows
- Fix integration issues

### Step 5: Documentation
- Document all public APIs
- Add usage examples
- Create troubleshooting guide

---

## 📊 Success Criteria

### Functional Requirements
- ✅ Store memories with metadata
- ✅ Search memories semantically
- ✅ Query knowledge graph
- ✅ Hybrid search combining both
- ✅ MCP tool integration
- ✅ Persistent storage

### Non-Functional Requirements
- ✅ < 100ms memory storage
- ✅ < 300ms hybrid search
- ✅ 100k+ memory capacity
- ✅ 80%+ test coverage
- ✅ Zero data loss
- ✅ Graceful error handling

---

## 🐛 Known Challenges & Solutions

### Challenge 1: Kuzu Python Bindings
**Issue**: Kuzu is relatively new, documentation may be sparse  
**Solution**: Use Kuzu examples, fallback to Neo4j if needed

### Challenge 2: Embedding Model Size
**Issue**: Sentence transformers models can be large  
**Solution**: Use lightweight model (all-MiniLM-L6-v2), cache downloads

### Challenge 3: Async ChromaDB
**Issue**: ChromaDB may not have full async support  
**Solution**: Use asyncio.to_thread() for blocking operations

### Challenge 4: Result Merging
**Issue**: Combining vector and graph results is complex  
**Solution**: Normalize scores, use weighted combination, deduplicate

---

## 📞 Next Steps

1. **Review this plan** - Ensure all requirements are captured
2. **Set up development environment** - Install dependencies
3. **Start implementation** - Follow the priority order
4. **Test continuously** - Write tests alongside code
5. **Document as you go** - Keep docs up to date
6. **Iterate and improve** - Refactor based on learnings

---

**Ready to implement? Switch to Code mode and start with `src/utils/config.py`!**
