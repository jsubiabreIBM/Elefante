import sys
import shutil
import time
from pathlib import Path

def factory_reset():
    print("WARNING: This will delete ALL Elefante memories!")
    print("There is no undo.")
    
    # Define paths
    home = Path.home() / ".elefante"
    data_dir = home / "data"
    chroma_dir = data_dir / "chroma"
    kuzu_dir = data_dir / "kuzu_db"
    
    print(f"\nTargeting:\n - {chroma_dir}\n - {kuzu_dir}")
    
    # Wipe Chroma
    if chroma_dir.exists():
        print("🗑️  Deleting ChromaDB...")
        try:
            shutil.rmtree(chroma_dir)
            print("✅ ChromaDB deleted.")
        except Exception as e:
            print(f"❌ Failed to delete Chroma: {e}")
            return False
    else:
        print("ℹ️  ChromaDB not found (clean).")

    # Wipe Kuzu
    if kuzu_dir.exists():
        print("🗑️  Deleting KuzuDB...")
        try:
            if kuzu_dir.is_file():
                kuzu_dir.unlink()
            else:
                shutil.rmtree(kuzu_dir)
            print("✅ KuzuDB deleted.")
        except Exception as e:
            print(f"❌ Failed to delete Kuzu: {e}")
            return False
    else:
        print("ℹ️  KuzuDB not found (clean).")
        
    print("\n✨ Factory Reset Complete. The slate is clean.")
    return True

if __name__ == "__main__":
    factory_reset()
