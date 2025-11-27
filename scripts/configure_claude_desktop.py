"""
Automatic Claude Desktop Configuration Script
Configures Claude Desktop to use Elefante MCP server
"""

import json
import os
from pathlib import Path

def get_claude_config_path():
    """Get the Claude Desktop config file path"""
    if os.name == 'nt':  # Windows
        appdata = os.environ.get('APPDATA')
        if not appdata:
            raise Exception("APPDATA environment variable not found")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    elif os.name == 'posix':  # macOS/Linux
        home = Path.home()
        if os.uname().sysname == 'Darwin':  # macOS
            return home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:  # Linux
            return home / ".config" / "Claude" / "claude_desktop_config.json"
    else:
        raise Exception(f"Unsupported operating system: {os.name}")

def configure_claude_desktop():
    """Configure Claude Desktop to use Elefante"""
    
    print("\n" + "="*60)
    print("🐘 ELEFANTE - Claude Desktop Configuration")
    print("="*60 + "\n")
    
    # Get paths
    config_path = get_claude_config_path()
    elefante_path = Path(__file__).parent.absolute()
    
    print(f"📁 Claude config: {config_path}")
    print(f"📁 Elefante path: {elefante_path}\n")
    
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing config or create new one
    if config_path.exists():
        print("📄 Loading existing Claude Desktop config...")
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        print("📄 Creating new Claude Desktop config...")
        config = {}
    
    # Ensure mcpServers section exists
    if 'mcpServers' not in config:
        config['mcpServers'] = {}
    
    # Add Elefante configuration
    config['mcpServers']['elefante'] = {
        "command": "python",
        "args": ["-m", "src.mcp.server"],
        "cwd": str(elefante_path).replace('\\', '\\\\'),
        "env": {
            "PYTHONPATH": str(elefante_path).replace('\\', '\\\\')
        }
    }
    
    # Save config
    print("💾 Saving configuration...")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Configuration complete!\n")
    print("="*60)
    print("📋 NEXT STEPS:")
    print("="*60)
    print("1. Restart Claude Desktop completely (close and reopen)")
    print("2. Look for 🔌 'Connected' indicator for Elefante")
    print("3. Test with: 'Remember that I'm Jaime from IBM Toronto'")
    print("4. Query with: 'What do you know about me?'")
    print("\n🎉 Elefante is ready to give Claude persistent memory!")
    print("="*60 + "\n")
    
    # Show the configuration
    print("📝 Configuration added:")
    print(json.dumps(config['mcpServers']['elefante'], indent=2))
    print()

if __name__ == "__main__":
    try:
        configure_claude_desktop()
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        print("Please configure manually using IDE_INTEGRATION_GUIDE.md")
        input("\nPress Enter to exit...")

# Made with Bob
