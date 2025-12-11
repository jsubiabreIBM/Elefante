#!/bin/bash
set -e

LOG_FILE="emergency_fix.log"
echo "Starting emergency fix at $(date)" > "$LOG_FILE"

PYTHON_EXEC="/opt/homebrew/bin/python3.11"

if [ ! -f "$PYTHON_EXEC" ]; then
    echo "Error: Python 3.11 not found at $PYTHON_EXEC" >> "$LOG_FILE"
    exit 1
fi

echo "Using Python: $PYTHON_EXEC" >> "$LOG_FILE"

# Create fresh venv
echo "Creating .venv_new..." >> "$LOG_FILE"
rm -rf .venv_new
"$PYTHON_EXEC" -m venv .venv_new

# Install dependencies
echo "Installing dependencies..." >> "$LOG_FILE"
./.venv_new/bin/pip install --upgrade pip >> "$LOG_FILE" 2>&1
./.venv_new/bin/pip install -r requirements.txt >> "$LOG_FILE" 2>&1

# Initialize DB
echo "Initializing databases..." >> "$LOG_FILE"
./.venv_new/bin/python scripts/init_databases.py >> "$LOG_FILE" 2>&1

# Swap venvs
echo "Swapping venvs..." >> "$LOG_FILE"
if [ -d ".venv" ]; then
    mv .venv .venv_old_$(date +%s) || rm -rf .venv
fi
mv .venv_new .venv

echo "Running health check..." >> "$LOG_FILE"
./.venv/bin/python scripts/health_check.py >> "$LOG_FILE" 2>&1

echo "SUCCESS" >> "$LOG_FILE"
