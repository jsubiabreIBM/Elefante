# Elefante Releases

**Versioning:** [Semantic Versioning 2.0.0](https://semver.org/)  
**Format:** MAJOR.MINOR.PATCH

---

## v1.0.0 - 2025-12-06 (Production Baseline)

**Status:** ✅ FUNCTIONAL  
**Tag:** `v1.0.0`

### What This Version Is
First stable production release after comprehensive cleanup and consolidation.

### Core Functionality
- **MCP Server:** 11 tools operational via stdio
- **ChromaDB:** Vector memory storage
- **Kuzu Graph:** Knowledge graph relationships
- **Dashboard:** React/Vite visualization

### Documentation State
- 5 Neural Registers (debug knowledge)
- 5 Domain Compendiums (issue tracking)
- Clean archive structure
- Single source of truth per topic

### Known Limitations
- MCP `searchMemories` occasionally returns empty (ChromaDB init timing)
- Dashboard requires hard refresh after builds (browser cache)
- Kuzu single-writer lock (one process at a time)
- Memory Schema V2 taxonomy requires manual input

---

## Version History (Pre-1.0 Development)

| Date | Internal Label | Notes |
|------|---------------|-------|
| 2025-11-27 | "v1.1.0" | Initial GitHub release |
| 2025-12-02 | "v1.2.0" | User profile integration |
| 2025-12-04 | "v1.2.0" | Kuzu reserved word fix |
| 2025-12-05 | "v1.3.0" | Cleanup session |
| 2025-12-06 | **v1.0.0** | Official baseline release |

**Note:** Pre-1.0 version numbers were inflated during rapid development. 
This release resets to proper semantic versioning starting at 1.0.0.

---

## Versioning Rules

### When to Increment

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fix (no API change) | PATCH (1.0.x) | Fix ChromaDB timing issue |
| New feature (backward compatible) | MINOR (1.x.0) | Add memory consolidation tool |
| Breaking API change | MAJOR (x.0.0) | Change MCP tool signatures |

### Release Checklist

1. Update CHANGELOG.md with new version section
2. Update this file with new version section
3. Run functional tests
4. Commit with message `release: vX.Y.Z`
5. Create git tag: `git tag vX.Y.Z -m "Release vX.Y.Z"`
6. Push tag: `git push origin vX.Y.Z`
