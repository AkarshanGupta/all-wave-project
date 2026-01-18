#!/bin/bash
set -e

# Run migrations
python run_migrations.py

# Start Uvicorn with proper host/port binding for Render
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
