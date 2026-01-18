#!/bin/bash
set -e

cd "$(dirname "$0")" || exit 1

# Run migrations
python run_migrations.py

# Start the application
python wsgi.py
