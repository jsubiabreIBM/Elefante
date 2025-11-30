"""
MCP Server Verification Script
------------------------------
Launches the MCP server as a subprocess and verifies it responds to JSON-RPC.
"""

import subprocess
import json
import sys
import time
import os
from pathlib import Path

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def test_mcp_server():
    log("🚀 Starting MCP Server Test...")
    
    # Path to server module
    server_cmd = [sys.executable, "-m", "src.mcp.server"]
    cwd = str(Path(__file__).parent.parent.absolute())
    
    # Add PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = cwd
    
    log(f"   Command: {' '.join(server_cmd)}")
    log(f"   CWD: {cwd}")
    
    try:
        # Start server process
        process = subprocess.Popen(
            server_cmd,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0 # Unbuffered
        )
        
        log("   ✅ Server process started.")
        
        # Prepare initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "ElefanteVerifier",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send request
        log("   📤 Sending 'initialize' request...")
        json_req = json.dumps(init_request) + "\n"
        process.stdin.write(json_req)
        process.stdin.flush()
        
        # Read response
        log("   📥 Waiting for response...")
        
        # Simple read loop with timeout
        start_time = time.time()
        response_line = None
        
        while time.time() - start_time < 10: # 10s timeout
            line = process.stdout.readline()
            if line:
                response_line = line
                break
            time.sleep(0.1)
            
        if response_line:
            log(f"   ✅ Received response: {response_line.strip()[:100]}...")
            
            try:
                response = json.loads(response_line)
                if "result" in response and "capabilities" in response["result"]:
                    log("   ✅ Server returned capabilities.")
                    log(f"   Server Name: {response['result']['serverInfo']['name']}")
                    return True
                else:
                    log("   ❌ Invalid response format.")
                    return False
            except json.JSONDecodeError:
                log("   ❌ Failed to decode JSON response.")
                return False
        else:
            log("   ❌ Timed out waiting for response.")
            # Check stderr
            stderr_out = process.stderr.read()
            if stderr_out:
                log(f"   ⚠️  Server Stderr: {stderr_out}")
            return False
            
    except Exception as e:
        log(f"   ❌ Test failed: {e}")
        return False
    finally:
        if 'process' in locals() and process.poll() is None:
            process.terminate()
            log("   🛑 Server process terminated.")

if __name__ == "__main__":
    if test_mcp_server():
        print("\n✅ MCP Server is functioning correctly.")
        sys.exit(0)
    else:
        print("\n❌ MCP Server test failed.")
        sys.exit(1)
