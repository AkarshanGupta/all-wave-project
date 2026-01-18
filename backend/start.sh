#!/bin/bash
set -e

# Run migrations
python run_migrations.py

# Start Uvicorn with proper host/port binding for Render
# Binds to 0.0.0.0 (required by Render) and uses PORT environment variable (default 10000)
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
