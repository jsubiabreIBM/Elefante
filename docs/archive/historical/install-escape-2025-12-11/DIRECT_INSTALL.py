#!/usr/bin/env python3.11
"""
Direct installation using system Python 3.11
Bypasses workspace environment completely
"""
import subprocess
import os
import sys
import shutil

workspace_dir = "/Volumes/X10Pro/X10-2025/Documents2025/Elefante_early_dec2025"
python311 = "/opt/homebrew/bin/python3.11"

def run_command(cmd, description=""):
    """Execute command and return result"""
    print(f"\n{'=' * 70}")
    if description:
        print(f"{description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'=' * 70}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=workspace_dir)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"STDERR: {result.stderr}")
    
    return result

def main():
    os.chdir(workspace_dir)
    print(f"Working from: {os.getcwd()}")
    print(f"Using Python: {python311}")
    
    # Step 1: Delete .venv
    print(f"\n{'#' * 70}")
    print("# STEP 1: Deleting broken .venv directory")
    print(f"{'#' * 70}")
    if os.path.exists(".venv"):
        shutil.rmtree(".venv", ignore_errors=True)
        print("✓ .venv directory deleted")
    else:
        print("✓ .venv already removed")
    
    # Step 2: Create venv
    print(f"\n{'#' * 70}")
    print("# STEP 2: Creating fresh Python 3.11 virtual environment")
    print(f"{'#' * 70}")
    result = run_command([python311, "-m", "venv", ".venv"])
    if result.returncode != 0:
        print(f"✗ FAILED to create venv")
        return False
    print("✓ Virtual environment created")
    
    # Step 3: Install dependencies
    print(f"\n{'#' * 70}")
    print("# STEP 3: Installing dependencies")
    print(f"{'#' * 70}")
    pip_path = os.path.join(workspace_dir, ".venv", "bin", "pip")
    result = run_command([pip_path, "install", "-r", "requirements.txt"],
                        "Installing packages from requirements.txt")
    if result.returncode != 0:
        print(f"✗ FAILED to install dependencies")
        return False
    print("✓ Dependencies installed")
    
    # Step 4: Initialize databases
    print(f"\n{'#' * 70}")
    print("# STEP 4: Initializing databases")
    print(f"{'#' * 70}")
    python_path = os.path.join(workspace_dir, ".venv", "bin", "python")
    result = run_command([python_path, "scripts/init_databases.py"],
                        "Running database initialization script")
    if result.returncode != 0:
        print(f"✗ FAILED to initialize databases")
        return False
    print("✓ Databases initialized")
    
    # Step 5: Health check
    print(f"\n{'#' * 70}")
    print("# STEP 5: Running health check")
    print(f"{'#' * 70}")
    result = run_command([python_path, "scripts/health_check.py"],
                        "Running health check script")
    
    print(f"\n{'#' * 70}")
    print("# FINAL STATUS")
    print(f"{'#' * 70}")
    if result.returncode == 0:
        print("✓✓✓ ALL STEPS COMPLETED SUCCESSFULLY ✓✓✓")
        print(f"Return code: {result.returncode}")
        return True
    else:
        print(f"✗✗✗ HEALTH CHECK FAILED ✗✗✗")
        print(f"Return code: {result.returncode}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
