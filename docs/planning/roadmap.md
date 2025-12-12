# Elefante Development Roadmap

**Current Version**: v1.0.0  
**Last Updated**: 2025-12-10

---

##  CRITICAL: Production Testing Findings (2025-12-10)

**Real-world testing revealed fundamental design flaws that MUST be addressed before v1.1.0:**

| Issue | Severity | Impact |
|-------|----------|--------|
| **Response Bloat** | CRITICAL | `elefanteMemorySearch` returns ~500 tokens/memory (90% nulls) - wastes context window |
| **Low Similarity Scores** | HIGH | Exact topic matches score 0.37-0.39 (should be 0.7+) - retrieval broken |
| **No Action Guidance** | HIGH | Raw JSON dump with no summary - agent can't use results effectively |

**Source**: See `docs/debug/memory/memory-compendium.md` Issues #7, #8, #9

**Priority**: These MUST be fixed before any new feature work.

---

## Current State (v1.0.0)

###  Implemented Features
- **Cognitive Memory Model** - LLM extracts emotional context, intent, entities, relationships
- **Temporal Decay** - Memories decay over time, reinforced on access
- **Dual Storage** - ChromaDB (vectors) + Kuzu (graph)
- **MCP Server** - 15 tools for IDE integration
- **Dashboard** - React/Vite visualization (functional but needs UX work)

###  Partial Implementation
- **Memory Schema V2** - Schema defined, but 3-level taxonomy (domain/category) defaults only
  - `domain` always defaults to `REFERENCE`
  - `category` always defaults to `general`
  - LLM does NOT auto-classify these fields

---

## Next Phase: v1.1.0 - Complete Schema V2

### Priority 1: Auto-Classification (HIGH)
**Goal**: LLM automatically detects domain and category

#### 1. Enhanced LLM Extraction
**Goal**: Deeper semantic understanding of memories

**Tasks**:
- [ ] Implement advanced `analyze_memory` function
  - Extract complex relationships (not just entities)
  - Identify temporal patterns (before/after, cause/effect)
  - Detect contradictions with existing memories
  - Extract implicit knowledge (assumptions, implications)

**Technical Approach**:
- Enhance LLM prompts for deeper analysis
- Add multi-pass extraction (entities -> relationships -> implications)
- Implement confidence scoring for extracted information

#### 2. Smart UPDATE (Merge Logic)
**Goal**: Intelligently merge new information with existing memories

**Tasks**:
- [ ] Update `llm.py` prompt to detect domain (work/personal/learning/project/reference)
- [ ] Update `llm.py` prompt to suggest category based on content
- [ ] Update `orchestrator.py` to apply LLM suggestions to metadata

**Files to Modify**:
- `src/core/llm.py` - Add domain/category to analysis prompt
- `src/core/orchestrator.py` - Apply extracted domain/category

---

### Priority 2: Smart UPDATE (MEDIUM)
**Goal**: Merge new info with existing memories instead of duplicating

**Tasks**:
- [ ] Implement UPDATE action in orchestrator (currently only ADD/IGNORE work)
- [ ] Merge metadata when similarity > 0.85
- [ ] Track version history

**Files to Modify**:
- `src/core/orchestrator.py` - Implement UPDATE branch
- `src/models/memory.py` - Add version tracking

---

### Priority 3: Dashboard UX (MEDIUM)
**Goal**: Make visualization useful, not just "bag of dots"

**Current Problems**:
- No meaningful color coding
- Labels are "salad" at scale
- Connections feel arbitrary

**Tasks**:
- [ ] Implement semantic zoom (hide labels at low zoom)
- [ ] Color by memory type or domain
- [ ] Show only high-importance nodes by default

**Files to Modify**:
- `src/dashboard/ui/src/components/GraphCanvas.tsx`

---

## Future Phases

### v1.2.0 - Smart Relationships
- Automatic relationship inference (if A->B and B->C, suggest A->C)
- Knowledge clustering
- Contradiction detection

### v1.3.0 - Multi-Modal
- Image memory support
- Audio transcription integration

---

## Historical Reference

Previous roadmap content archived at: `docs/archive/historical/task-roadmap-completed.md`

---

**Last Updated**: 2025-12-03  
**Status**: Planning Phase  
**Target Release**: v1.2.0 (TBD)

---

For current development status, see [`docs/debug/general/task-roadmap.md`](docs/debug/general/task-roadmap.md)