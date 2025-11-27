"""
Elefante Unified Installation Script
------------------------------------
Robust, one-click installation for Windows, macOS, and Linux.
Handles:
1. Virtual Environment creation
2. Dependency installation
3. Database initialization
4. MCP Server configuration (VSCode/Bob)
5. System verification
"""

import os
import sys
import subprocess
import platform
import json
import shutil
import argparse
import datetime
from pathlib import Path

# Ensure we can import from scripts directory
sys.path.append(str(Path(__file__).parent))

# Import existing configuration logic
try:
    from configure_vscode_bob import configure_mcp
except ImportError:
    # Fallback if running from root
    sys.path.append(str(Path(__file__).parent / "scripts"))
    from configure_vscode_bob import configure_mcp

class Logger:
    def __init__(self, log_file=None):
        self.log_file = log_file
        if log_file:
            # Ensure log file exists and is writable
            try:
                with open(log_file, 'a', encoding='utf-8') as f:
                    pass
            except Exception as e:
                print(f"⚠️  Could not open log file {log_file}: {e}")
                self.log_file = None

    def log(self, msg, end="\n"):
        # Print to console
        print(msg, end=end)
        # Write to file if configured
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    # Strip ANSI color codes if we were using them (we aren't much, but good practice)
                    clean_msg = msg
                    f.write(clean_msg + end)
            except Exception:
                pass

logger = None

def print_header(msg):
    logger.log("\n" + "="*60)
    logger.log(f"🐘 {msg}")
    logger.log("="*60 + "\n")

def print_step(step, msg):
    logger.log(f"\n[Step {step}] {msg}...")

def run_command(cmd, cwd=None, shell=False):
    """Run a command and check for errors"""
    try:
        # We want to capture output to log it, but also show it in real-time.
        # For simplicity in this script, we let subprocess write to stdout/stderr,
        # which means it goes to console.
        # If we have a log file, we really should capture it.
        if logger.log_file:
            # Use Popen to capture and log line by line
            process = subprocess.Popen(
                cmd, 
                cwd=cwd, 
                shell=shell, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    logger.log(line.rstrip())
            
            return process.poll() == 0
        else:
            subprocess.check_call(cmd, cwd=cwd, shell=shell)
            return True
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        logger.log(f"❌ Execution error: {e}")
        return False

def get_python_cmd():
    """Get the correct python command"""
    if sys.platform == 'win32':
        return sys.executable
    return sys.executable

def create_venv(root_dir):
    """Create virtual environment if it doesn't exist"""
    venv_dir = root_dir / ".venv"
    if venv_dir.exists():
        logger.log("✅ Virtual environment already exists.")
        return True
    
    logger.log("📦 Creating virtual environment...")
    if run_command([sys.executable, "-m", "venv", ".venv"], cwd=root_dir):
        logger.log("✅ Virtual environment created.")
        return True
    else:
        logger.log("❌ Failed to create virtual environment.")
        return False

def install_dependencies(root_dir, python_cmd):
    """Install requirements.txt"""
    logger.log("📥 Installing dependencies...")
    
    # Upgrade pip
    run_command([python_cmd, "-m", "pip", "install", "--upgrade", "pip"], cwd=root_dir)
    
    # Install requirements
    if run_command([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"], cwd=root_dir):
        logger.log("✅ Dependencies installed.")
        return True
    else:
        logger.log("❌ Failed to install dependencies.")
        return False

def init_databases(root_dir, python_cmd):
    """Initialize ChromaDB and Kuzu"""
    logger.log("💽 Initializing databases...")
    script_path = root_dir / "scripts" / "init_databases.py"
    if run_command([python_cmd, str(script_path)], cwd=root_dir):
        logger.log("✅ Databases initialized.")
        return True
    else:
        logger.log("❌ Database initialization failed.")
        return False

def run_health_check(root_dir, python_cmd):
    """Run health check script"""
    logger.log("🏥 Running health check...")
    script_path = root_dir / "scripts" / "health_check.py"
    if run_command([python_cmd, str(script_path)], cwd=root_dir):
        logger.log("✅ Health check passed.")
        return True
    else:
        logger.log("❌ Health check failed.")
        return False

def generate_proof(root_dir, success):
    """Generate installation proof block"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    
    proof = f"""
============================================================
📜 INSTALLATION PROOF
============================================================
Date:   {timestamp}
Status: {status}
Path:   {root_dir}
System: {platform.system()} {platform.release()}
============================================================
"""
    logger.log(proof)
    return proof

def main():
    global logger
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-file", help="Path to log file")
    args = parser.parse_args()
    
    logger = Logger(args.log_file)
    
    root_dir = Path(__file__).parent.parent.absolute()
    os.chdir(root_dir)
    
    print_header("ELEFANTE INSTALLATION WIZARD")
    logger.log(f"📂 Installation Directory: {root_dir}")
    logger.log(f"🐍 Python: {sys.version.split()[0]}")
    
    success = True
    
    # 1. Virtual Environment
    print_step(1, "Environment Setup")
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv:
        logger.log("⚠️  Not running in a virtual environment.")
        logger.log("   It is recommended to run this script via 'install.bat' (Windows) or 'install.sh' (Mac/Linux).")
    
    python_cmd = get_python_cmd()
    
    # 2. Dependencies
    print_step(2, "Dependencies")
    if not install_dependencies(root_dir, python_cmd):
        success = False
    
    if success:
        # 3. Databases
        print_step(3, "Database Initialization")
        if not init_databases(root_dir, python_cmd):
            success = False
            
    if success:
        # 4. MCP Configuration
        print_step(4, "IDE Configuration")
        try:
            if configure_mcp():
                logger.log("✅ MCP Server configured for VSCode/Bob.")
            else:
                logger.log("⚠️  MCP Configuration skipped or failed (check logs above).")
        except Exception as e:
            logger.log(f"❌ Error configuring MCP: {e}")
            
    if success:
        # 5. Verification
        print_step(5, "System Verification")
        if not run_health_check(root_dir, python_cmd):
            logger.log("⚠️  Health check failed. Please review the errors.")
            success = False
    
    # Generate Proof
    generate_proof(root_dir, success)
    
    if success:
        print_header("INSTALLATION COMPLETE! 🎉")
        logger.log("Next Steps:")
        logger.log("1. Restart your IDE (VSCode/Bob) to load the MCP server.")
        logger.log("2. Start using Elefante commands in your AI chat!")
        logger.log("   - 'Remember that...'\n   - 'What do you know about...'\n")
    else:
        print_header("INSTALLATION FAILED ❌")
        logger.log("Please check the logs above for errors.")
        sys.exit(1)
    
    if os.name == 'nt':
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
