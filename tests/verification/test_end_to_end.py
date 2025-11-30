"""
Elefante End-to-End Test Script
-------------------------------
Simulates a full MCP client session:
1. Starts the server
2. Initializes connection
3. Calls 'addMemory' to store a test fact
4. Calls 'searchMemories' to retrieve it
5. Verifies the result
"""

import subprocess
import json
import sys
import time
import os
from pathlib import Path

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def read_json_rpc(process, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        line = process.stdout.readline()
        if line:
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                log(f"   ⚠️  Ignored non-JSON output: {line.strip()}")
        time.sleep(0.01)
    return None

def send_request(process, method, params=None, req_id=1):
    req = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": method
    }
    if params:
        req["params"] = params
    
    json_req = json.dumps(req) + "\n"
    process.stdin.write(json_req)
    process.stdin.flush()
    return req_id

def test_end_to_end():
    log("🚀 Starting End-to-End Test...")
    
    # Setup paths
    cwd = str(Path(__file__).parent.parent.absolute())
    server_cmd = [sys.executable, "-m", "src.mcp.server"]
    env = os.environ.copy()
    env["PYTHONPATH"] = cwd
    
    process = None
    try:
        # 1. Start Server
        log("   Starting server process...")
        process = subprocess.Popen(
            server_cmd,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=sys.stderr, # Pass stderr through to console
            text=True,
            bufsize=0
        )
        
        # 2. Initialize
        log("   📤 Sending 'initialize'...")
        send_request(process, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "E2ETester", "version": "1.0"}
        }, req_id=1)
        
        resp = read_json_rpc(process)
        if not resp or "result" not in resp:
            log("   ❌ Initialization failed.")
            return False
        log("   ✅ Initialized.")
        
        # 3. Add Memory
        test_content = f"Elefante E2E Test Memory {int(time.time())}"
        log(f"   📤 Adding memory: '{test_content}'...")
        
        send_request(process, "tools/call", {
            "name": "addMemory",
            "arguments": {
                "content": test_content,
                "importance": 10,
                "tags": ["test", "e2e"]
            }
        }, req_id=2)
        
        resp = read_json_rpc(process, timeout=15) # Give it time to embed
        if not resp or "result" not in resp:
            log("   ❌ addMemory failed or timed out.")
            return False
            
        # Parse inner tool result
        tool_result = resp["result"]
        # MCP tool results are wrapped in content list
        if "content" in tool_result:
            inner_json = tool_result["content"][0]["text"]
            inner_data = json.loads(inner_json)
            if inner_data.get("success"):
                log("   ✅ Memory stored successfully.")
            else:
                log(f"   ❌ addMemory reported failure: {inner_data}")
                return False
        
        # 4. Search Memory
        log(f"   📤 Searching for memory with query: '{test_content}'...")
        send_request(process, "tools/call", {
            "name": "searchMemories",
            "arguments": {
                "query": test_content, # Use exact content for better match
                "limit": 5
            }
        }, req_id=3)
        
        resp = read_json_rpc(process, timeout=10)
        if not resp or "result" not in resp:
            log("   ❌ searchMemories failed.")
            return False
            
        tool_result = resp["result"]
        if "content" in tool_result:
            inner_json = tool_result["content"][0]["text"]
            inner_data = json.loads(inner_json)
            results = inner_data.get("results", [])
            
            log(f"   🔎 Found {len(results)} results.")
            if len(results) > 0:
                log(f"   First result raw: {json.dumps(results[0], default=str)}")
            
            found = False
            for i, res in enumerate(results):
                content = res.get('content') or res.get('text') or str(res)
                log(f"      [{i}] {content[:50]}...")
                if test_content in content:
                    found = True
            
            if found:
                log(f"   ✅ Found memory: '{test_content}'")
                return True
            else:
                log(f"   ❌ Memory not found in top {len(results)} results.")
                return False
                
    except Exception as e:
        log(f"   ❌ Test exception: {e}")
        return False
    finally:
        if process:
            process.terminate()
            log("   🛑 Server terminated.")

if __name__ == "__main__":
    if test_end_to_end():
        print("\n✅ End-to-End Test PASSED")
        sys.exit(0)
    else:
        print("\n❌ End-to-End Test FAILED")
        sys.exit(1)