"""
Verify that the Elefante repository is clean and ready for GitHub.
Checks for leftover files, test artifacts, and proper organization.
"""

import os
import sys
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_clean_repo():
    """Verify repository cleanliness"""
    
    print("\n" + "="*70)
    print("ELEFANTE REPOSITORY CLEANLINESS CHECK")
    print("="*70 + "\n")
    
    issues = []
    warnings = []
    
    # Check for data directory
    if Path("data").exists():
        issues.append("ERROR: data/ directory exists (should be gitignored)")
    else:
        print("OK: No data/ directory (clean)")
    
    # Check for logs directory
    if Path("logs").exists():
        issues.append("ERROR: logs/ directory exists (should be gitignored)")
    else:
        print("OK: No logs/ directory (clean)")
    
    # Check for __pycache__
    pycache_dirs = list(Path(".").rglob("__pycache__"))
    if pycache_dirs:
        issues.append(f"ERROR: Found {len(pycache_dirs)} __pycache__ directories")
    else:
        print("OK: No __pycache__ directories (clean)")
    
    # Check for .pyc files
    pyc_files = list(Path(".").rglob("*.pyc"))
    if pyc_files:
        issues.append(f"ERROR: Found {len(pyc_files)} .pyc files")
    else:
        print("OK: No .pyc files (clean)")
    
    # Check for .env file
    if Path(".env").exists():
        warnings.append("WARN: .env file exists (should be .env.example only)")
    else:
        print("OK: No .env file (use .env.example)")
    
    # Check for proper structure
    required_dirs = ["src", "scripts", "docs", "examples", "tests"]
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"OK: {dir_name}/ directory exists")
        else:
            issues.append(f"ERROR: Missing {dir_name}/ directory")
    
    # Check for required files
    required_files = [
        "README.md",
        "LICENSE",
        "requirements.txt",
        "setup.py",
        ".gitignore",
        "CONTRIBUTING.md",
        "CHANGELOG.md"
    ]
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"OK: {file_name} exists")
        else:
            issues.append(f"ERROR: Missing {file_name}")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if not issues and not warnings:
        print("\nOK: Repository is clean and ready")
        print("OK: All checks passed")
        print("OK: No test artifacts found")
        print("OK: Proper structure verified")
        print("OK: All required files present")
        return 0
    
    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    if issues:
        print("\nISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
        print("\nPlease fix these issues before pushing")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(check_clean_repo())

# Made with Bob
