
import sys
import os
import asyncio
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mcp.server import ElefanteMCPServer

def test_injection():
    server = ElefanteMCPServer()
    
    # Test case 1: Generic tool
    result = {"data": "some data"}
    injected = server._inject_pitfalls(result, "someTool")
    
    print("--- Test Case 1: Generic Tool ---")
    print(json.dumps(injected, indent=2))
    
    if "🛑_MANDATORY_PROTOCOLS_READ_THIS_FIRST" in injected:
        print("✅ Injection successful")
    else:
        print("❌ Injection failed")

    # Test case 2: searchMemories
    result_search = {"results": []}
    injected_search = server._inject_pitfalls(result_search, "searchMemories")
    
    print("\n--- Test Case 2: searchMemories ---")
    print(json.dumps(injected_search, indent=2))
    
    protocols = injected_search.get("🛑_MANDATORY_PROTOCOLS_READ_THIS_FIRST", [])
    if any("SEARCH BIAS" in p for p in protocols):
        print("✅ Context-specific injection successful")
    else:
        print("❌ Context-specific injection failed")

if __name__ == "__main__":
    # Mock the _register_handlers to avoid async issues during init if any
    # But init calls _register_handlers which is sync (it defines async functions but doesn't run them)
    # So it should be fine.
    test_injection()
