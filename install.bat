@echo off
REM Elefante One-Click Installer for Windows
REM ========================================

setlocal enabledelayedexpansion

echo ============================================================
echo 🐘 ELEFANTE INSTALLER
echo ============================================================
echo.

REM 1. Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

REM 2. Create Virtual Environment
if not exist .venv (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM 3. Activate Virtual Environment
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

REM 4. Run Python Installer
echo [INFO] Starting installation wizard...
python scripts\install.py

REM Keep window open if run from explorer
echo.
pause
