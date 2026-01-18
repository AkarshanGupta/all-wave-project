"""
Automated migration runner for production deployment.
Run this script once during deployment to apply all pending migrations.
"""

import logging
from alembic.config import Config
from alembic.command import upgrade
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run all pending Alembic migrations."""
    try:
        # Get the alembic config file
        alembic_cfg = Config("alembic.ini")
        
        # Ensure the database URL is set from environment
        from app.core.config import settings
        alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
        
        logger.info("Starting database migrations...")
        logger.info(f"Database: {settings.database_url}")
        
        # Upgrade to the latest revision
        upgrade(alembic_cfg, "head")
        
        logger.info("✓ Migrations completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_migrations()
    exit(0 if success else 1)
