#!/bin/bash
# Production migration script for Linux/Mac deployment

set -e

echo "🔄 Running database migrations..."
python run_migrations.py

if [ $? -eq 0 ]; then
    echo "✓ Migrations completed. Starting application..."
else
    echo "✗ Migrations failed. Aborting deployment."
    exit 1
fi
