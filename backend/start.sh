#!/bin/bash
set -e

# Run migrations
python run_migrations.py

# Start the application (will bind to 0.0.0.0 and PORT environment variable)
python app/main.py
