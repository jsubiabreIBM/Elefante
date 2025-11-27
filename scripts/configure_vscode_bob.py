"""
Automatic VSCode/Bob MCP Configuration Script
Configures VSCode (Bob fork) to use Elefante MCP server automatically
"""

import json
import os
import sys
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def get_vscode_settings_path():
    """Get the VSCode settings.json path"""
    if os.name == 'nt':  # Windows
        appdata = os.environ.get('APPDATA')
        if not appdata:
            raise Exception("APPDATA environment variable not found")
        return Path(appdata) / "Code" / "User" / "settings.json"
    elif os.name == 'posix':  # macOS/Linux
        home = Path.home()
        if os.uname().sysname == 'Darwin':  # macOS
            return home / "Library" / "Application Support" / "Code" / "User" / "settings.json"
        else:  # Linux
            return home / ".config" / "Code" / "User" / "settings.json"
    else:
        raise Exception(f"Unsupported operating system: {os.name}")

def configure_vscode_mcp():
    """Configure VSCode/Bob to use Elefante MCP server"""
    
    print("\n" + "="*70)
    print("🐘 ELEFANTE - VSCode/Bob MCP Configuration")
    print("="*70 + "\n")
    
    # Get paths
    settings_path = get_vscode_settings_path()
    elefante_path = Path(__file__).parent.absolute()
    
    print(f"📁 VSCode settings: {settings_path}")
    print(f"📁 Elefante path: {elefante_path}\n")
    
    # Load existing settings
    if not settings_path.exists():
        print("❌ VSCode settings.json not found!")
        print(f"Expected location: {settings_path}")
        return False
    
    print("📄 Loading VSCode settings...")
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    
    # Ensure MCP is enabled
    if not settings.get('chat.mcp.gallery.enabled'):
        print("⚠️  MCP gallery not enabled. Enabling it now...")
        settings['chat.mcp.gallery.enabled'] = True
    
    # Add MCP servers configuration
    if 'chat.mcp.servers' not in settings:
        settings['chat.mcp.servers'] = {}
    
    # Configure Elefante MCP server
    elefante_config = {
        "command": "python",
        "args": ["-m", "src.mcp.server"],
        "cwd": str(elefante_path),
        "env": {
            "PYTHONPATH": str(elefante_path)
        },
        "autoStart": True  # Auto-start when VSCode opens!
    }
    
    settings['chat.mcp.servers']['elefante'] = elefante_config
    
    # Save settings
    print("💾 Saving configuration...")
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)
    
    print("\n✅ Configuration complete!\n")
    print("="*70)
    print("📋 CONFIGURATION ADDED:")
    print("="*70)
    print(json.dumps(elefante_config, indent=2))
    print("\n" + "="*70)
    print("🎯 NEXT STEPS:")
    print("="*70)
    print("1. ✅ Restart VSCode/Bob (close and reopen)")
    print("2. ✅ Elefante will auto-start with the AI assistant")
    print("3. ✅ Test: Ask Bob 'Remember that I'm Jaime from IBM Toronto'")
    print("4. ✅ Query: Ask Bob 'What do you know about me?'")
    print("\n🎉 Elefante will now give Bob persistent memory automatically!")
    print("="*70 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        success = configure_vscode_mcp()
        if success:
            print("✅ Setup successful! Restart VSCode/Bob to activate Elefante.\n")
        else:
            print("❌ Setup failed. Please check the error messages above.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        print("Please configure manually - see VSCODE_BOB_SETUP.md")
    
    input("Press Enter to exit...")

# Made with Bob
