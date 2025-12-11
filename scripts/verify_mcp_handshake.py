import sys
import asyncio
import json
import subprocess
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.utils.logger import get_logger

logger = get_logger("verification")

async def verify_handshake():
    """
    Simulates a real MCP connection handshake.
    1. Starts the server process.
    2. Sends 'initialize' JSON-RPC request.
    3. Expects valid 'initialize' result with capabilities.
    4. Sends 'notifications/initialized'.
    5. Validates server is truly responsive (not just a running process).
    """
    logger.info("🔌 Testing MCP Server Handshake...")
    
    server_script = project_root / "src" / "mcp" / "server.py"
    cmd = [sys.executable, "-m", "src.mcp.server"]
    
    try:
        # Start Server Process
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(project_root),
            env={"PYTHONPATH": str(project_root)}  # Essential for imports
        )
        
        # 1. Send Initialize Request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "ElefanteVerifier", "version": "1.0"}
            }
        }
        
        logger.info("📤 Sending 'initialize'...")
        process.stdin.write(json.dumps(init_request).encode() + b"\n")
        await process.stdin.drain()
        
        # 2. Read Response (with timeout)
        try:
            line = await asyncio.wait_for(process.stdout.readline(), timeout=10.0)
        except asyncio.TimeoutError:
            logger.error("❌ Timeout waiting for 'initialize' response")
            process.kill()
            return False
            
        if not line:
            stderr = await process.stderr.read()
            logger.error(f"❌ Server closed connection unexpectedly.\nStderr: {stderr.decode()}")
            return False
            
        response = json.loads(line.decode())
        
        # 3. Validate Response
        if response.get("id") != 1:
            logger.error(f"❌ ID mismatch. Expected 1, got {response.get('id')}")
            return False
            
        if "result" not in response:
            logger.error(f"❌ Invalid response format: {response}")
            return False
            
        capabilities = response["result"].get("capabilities", {})
        logger.info(f"✅ Handshake OK! Server Capabilities: {list(capabilities.keys())}")
        
        # 4. Send Initialized Notification
        logger.info("📤 Sending 'notifications/initialized'...")
        notify_msg = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        process.stdin.write(json.dumps(notify_msg).encode() + b"\n")
        await process.stdin.drain()
        
        # Clean shutdown
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            process.kill()
            
        logger.info("✅ Verification Complete: MCP Server is speaking protocol.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Verification Failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(verify_handshake())
    if not success:
        sys.exit(1)
    sys.exit(0)
