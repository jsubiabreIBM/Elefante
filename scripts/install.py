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

def print_header(msg):
    print("\n" + "="*60)
    print(f"🐘 {msg}")
    print("="*60 + "\n")

def print_step(step, msg):
    print(f"\n[Step {step}] {msg}...")

def run_command(cmd, cwd=None, shell=False):
    """Run a command and check for errors"""
    try:
        subprocess.check_call(cmd, cwd=cwd, shell=shell)
        return True
    except subprocess.CalledProcessError:
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
        print("✅ Virtual environment already exists.")
        return True
    
    print("📦 Creating virtual environment...")
    if run_command([sys.executable, "-m", "venv", ".venv"], cwd=root_dir):
        print("✅ Virtual environment created.")
        return True
    else:
        print("❌ Failed to create virtual environment.")
        return False

def install_dependencies(root_dir, python_cmd):
    """Install requirements.txt"""
    print("📥 Installing dependencies...")
    
    # Upgrade pip
    run_command([python_cmd, "-m", "pip", "install", "--upgrade", "pip"], cwd=root_dir)
    
    # Install requirements
    if run_command([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"], cwd=root_dir):
        print("✅ Dependencies installed.")
        return True
    else:
        print("❌ Failed to install dependencies.")
        return False

def init_databases(root_dir, python_cmd):
    """Initialize ChromaDB and Kuzu"""
    print("💽 Initializing databases...")
    script_path = root_dir / "scripts" / "init_databases.py"
    if run_command([python_cmd, str(script_path)], cwd=root_dir):
        print("✅ Databases initialized.")
        return True
    else:
        print("❌ Database initialization failed.")
        return False

def run_health_check(root_dir, python_cmd):
    """Run health check script"""
    print("🏥 Running health check...")
    script_path = root_dir / "scripts" / "health_check.py"
    if run_command([python_cmd, str(script_path)], cwd=root_dir):
        print("✅ Health check passed.")
        return True
    else:
        print("❌ Health check failed.")
        return False

def main():
    root_dir = Path(__file__).parent.parent.absolute()
    os.chdir(root_dir)
    
    print_header("ELEFANTE INSTALLATION WIZARD")
    print(f"📂 Installation Directory: {root_dir}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # 1. Virtual Environment
    print_step(1, "Environment Setup")
    # Note: If we are already running inside the venv (which the bat/sh script should ensure),
    # we don't need to create it. But if run directly with system python, we might want to.
    # For simplicity, we assume the wrapper script handles the venv activation or we use the current python.
    # However, to be truly robust, we should check if we are in a venv.
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv:
        print("⚠️  Not running in a virtual environment.")
        print("   It is recommended to run this script via 'install.bat' (Windows) or 'install.sh' (Mac/Linux).")
        # We proceed anyway using the current python
    
    python_cmd = get_python_cmd()
    
    # 2. Dependencies
    print_step(2, "Dependencies")
    if not install_dependencies(root_dir, python_cmd):
        sys.exit(1)
        
    # 3. Databases
    print_step(3, "Database Initialization")
    if not init_databases(root_dir, python_cmd):
        sys.exit(1)
        
    # 4. MCP Configuration
    print_step(4, "IDE Configuration")
    try:
        if configure_mcp():
            print("✅ MCP Server configured for VSCode/Bob.")
        else:
            print("⚠️  MCP Configuration skipped or failed (check logs above).")
    except Exception as e:
        print(f"❌ Error configuring MCP: {e}")
        
    # 5. Verification
    print_step(5, "System Verification")
    if not run_health_check(root_dir, python_cmd):
        print("⚠️  Health check failed. Please review the errors.")
        # Don't exit, as installation might still be mostly working
        
    print_header("INSTALLATION COMPLETE! 🎉")
    print("Next Steps:")
    print("1. Restart your IDE (VSCode/Bob) to load the MCP server.")
    print("2. Start using Elefante commands in your AI chat!")
    print("   - 'Remember that...'\n   - 'What do you know about...'\n")
    
    if os.name == 'nt':
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
