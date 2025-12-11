#!/usr/bin/env python3
"""Master script to run installation from system Python"""
import subprocess
import sys
import os

os.chdir("/Volumes/X10Pro/X10-2025/Documents2025/Elefante_early_dec2025")

print("="*70)
print("ELEFANTE AUTONOMOUS INSTALLATION - PYTHON 3.11")
print("="*70)
print()

# Execute the installation script
result = subprocess.run(
    ["/opt/homebrew/bin/python3.11", "DO_INSTALL.py"],
    cwd="/Volumes/X10Pro/X10-2025/Documents2025/Elefante_early_dec2025"
)

print()
print("="*70)
print(f"Installation complete with exit code: {result.returncode}")
print("="*70)

sys.exit(result.returncode)
