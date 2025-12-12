"""Automatic VS Code/Bob MCP configuration.

Configures VS Code (including Insiders) and Bob-IDE to use the Elefante MCP server.
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

def get_settings_paths():
    """Get potential settings.json paths for VS Code, Cursor, and Bob-IDE."""
    paths = []
    
    if os.name == 'nt':  # Windows
        appdata = os.environ.get('APPDATA')
        if appdata:
            # Standard VSCode
            paths.append(Path(appdata) / "Code" / "User" / "settings.json")
            # VS Code Insiders
            paths.append(Path(appdata) / "Code - Insiders" / "User" / "settings.json")
            # Cursor
            paths.append(Path(appdata) / "Cursor" / "User" / "settings.json")
            # Bob-IDE (User provided path)
            paths.append(Path(appdata) / "Bob-IDE" / "User" / "globalStorage" / "ibm.bob-code" / "settings" / "mcp_settings.json")
            # Bob-IDE (Standard User settings)
            paths.append(Path(appdata) / "Bob-IDE" / "User" / "settings.json")
            
    elif os.name == 'posix':  # macOS/Linux
        home = Path.home()
        if os.uname().sysname == 'Darwin':  # macOS
            paths.append(home / "Library" / "Application Support" / "Code" / "User" / "settings.json")
            paths.append(home / "Library" / "Application Support" / "Code - Insiders" / "User" / "settings.json")
            paths.append(home / "Library" / "Application Support" / "Cursor" / "User" / "settings.json")
            paths.append(home / "Library" / "Application Support" / "Bob-IDE" / "User" / "settings.json")
        else:  # Linux
            paths.append(home / ".config" / "Code" / "User" / "settings.json")
            paths.append(home / ".config" / "Code - Insiders" / "User" / "settings.json")
            paths.append(home / ".config" / "Cursor" / "User" / "settings.json")
            paths.append(home / ".config" / "Bob-IDE" / "User" / "settings.json")
            
    return paths


def get_mcp_json_paths():
    """Get potential VS Code MCP configuration file paths (mcp.json)."""
    paths = []

    if os.name == 'nt':
        appdata = os.environ.get('APPDATA')
        if appdata:
            paths.append(Path(appdata) / "Code" / "User" / "mcp.json")
            paths.append(Path(appdata) / "Code - Insiders" / "User" / "mcp.json")
    elif os.name == 'posix':
        home = Path.home()
        if os.uname().sysname == 'Darwin':
            paths.append(home / "Library" / "Application Support" / "Code" / "User" / "mcp.json")
            paths.append(home / "Library" / "Application Support" / "Code - Insiders" / "User" / "mcp.json")
        else:
            paths.append(home / ".config" / "Code" / "User" / "mcp.json")
            paths.append(home / ".config" / "Code - Insiders" / "User" / "mcp.json")

    return paths


def configure_vscode_mcp_json(mcp_json_path: Path, elefante_path: Path) -> bool:
    """Add/update the Elefante server config in a VS Code mcp.json file."""
    try:
        mcp_json_path.parent.mkdir(parents=True, exist_ok=True)
        if mcp_json_path.exists():
            with open(mcp_json_path, 'r', encoding='utf-8') as f:
                config = json.load(f) or {}
        else:
            config = {}
    except Exception:
        config = {}

    if not isinstance(config, dict):
        config = {}

    if 'servers' not in config or not isinstance(config.get('servers'), dict):
        config['servers'] = {}

    config['servers']['elefante'] = {
        "type": "stdio",
        "command": sys.executable,
        "args": ["-m", "src.mcp.server"],
        "env": {
            "PYTHONPATH": str(elefante_path),
            "ELEFANTE_CONFIG_PATH": str(elefante_path / "config.yaml"),
            "ANONYMIZED_TELEMETRY": "False",
        },
    }

    try:
        with open(mcp_json_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False

def configure_mcp():
    """Configure IDE to use Elefante MCP server"""
    
    print("\n" + "=" * 70)
    print("ELEFANTE - IDE MCP Configuration")
    print("=" * 70 + "\n")
    
    # Get current Elefante path (AGNOSTIC)
    # We use the parent of the 'scripts' directory where this script resides
    elefante_path = Path(__file__).parent.parent.absolute()
    
    print(f"Elefante Location: {elefante_path}")

    # Configure VS Code MCP (mcp.json) when available
    mcp_paths = get_mcp_json_paths()
    mcp_configured = False
    for mcp_path in mcp_paths:
        if mcp_path.parent.exists():
            print(f"\nConfiguring VS Code MCP config: {mcp_path}")
            if configure_vscode_mcp_json(mcp_path, elefante_path):
                mcp_configured = True
            else:
                print(f"Warning: Failed to write {mcp_path}")
    
    # Find valid settings files
    potential_paths = get_settings_paths()
    found_paths = [p for p in potential_paths if p.exists()]
    
    if not found_paths and not mcp_configured:
        print("No compatible IDE settings found!")
        print("Checked locations:")
        for p in potential_paths:
            print(f" - {p}")
        for p in mcp_paths:
            print(f" - {p}")
        return False
        
    if found_paths:
        print(f"Found {len(found_paths)} IDE settings file(s).")
    
    # Configure each found settings file
    for settings_path in found_paths:
        print(f"\nConfiguring: {settings_path}")
        
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Error reading {settings_path}. Skipping.")
            continue
            
        # Determine config structure based on file type
        is_mcp_settings = "mcp_settings.json" in str(settings_path)
        
        # Prepare Elefante config
        elefante_config = {
            "command": sys.executable,
            "args": ["-m", "src.mcp.server"],
            "cwd": str(elefante_path),
            "env": {
                "PYTHONPATH": str(elefante_path),
                "ANONYMIZED_TELEMETRY": "False" # Disable ChromaDB telemetry
            },
            "disabled": False,
            "alwaysAllow": [
                "elefanteMemorySearch",
                "elefanteMemoryAdd",
                "elefanteSystemStatusGet",
                "elefanteDashboardOpen",
                "elefanteGraphConnect",
                "elefanteContextGet",
                "elefanteGraphEntityCreate",
                "elefanteGraphRelationshipCreate",
                "elefanteGraphQuery",
                "elefanteSystemEnable",
                "elefanteSystemDisable",
                "elefanteSessionsList",
                "elefanteMemoryListAll",
                "elefanteMemoryConsolidate",
                "elefanteMemoryMigrateToV3",
            ]
        }
        
        # Inject config
        if is_mcp_settings:
            # Bob-IDE specific mcp_settings.json structure
            if "mcpServers" not in settings:
                settings["mcpServers"] = {}
            settings["mcpServers"]["elefante"] = elefante_config
        else:
            # Standard VSCode settings.json structure
            if not settings.get('chat.mcp.gallery.enabled'):
                settings['chat.mcp.gallery.enabled'] = True
                
            if 'chat.mcp.servers' not in settings:
                settings['chat.mcp.servers'] = {}
            
            # VSCode uses a slightly different format for autoStart
            vscode_config = elefante_config.copy()
            vscode_config["autoStart"] = True
            settings['chat.mcp.servers']['elefante'] = vscode_config
            
        # Save settings
        print("Saving configuration...")
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4)
            
    print("\n" + "="*70)
    print("Configuration complete!")
    print("="*70)
    print("1. Restart your IDE")
    print("2. Elefante will auto-connect from:")
    print(f"   {elefante_path}")
    print("="*70 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        success = configure_mcp()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}\n")
        sys.exit(1)
