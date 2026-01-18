@echo off
REM Production migration script for Windows deployment

echo 🔄 Running database migrations...
python run_migrations.py

if errorlevel 1 (
    echo ✗ Migrations failed. Aborting deployment.
    exit /b 1
) else (
    echo ✓ Migrations completed. Starting application...
    exit /b 0
)
