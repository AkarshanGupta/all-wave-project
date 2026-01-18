"""
Automated migration runner for production deployment.
Run this script once during deployment to apply all pending migrations.
"""

import logging
import sys
from alembic.config import Config
from alembic.command import upgrade, current
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
        logger.info(f"Database URL configured")
        
        # Check current revision
        try:
            logger.info("Checking current database revision...")
            current(alembic_cfg)
        except Exception as e:
            logger.warning(f"Could not get current revision: {e}")
        
        # Upgrade to the latest revision
        logger.info("Applying all pending migrations...")
        upgrade(alembic_cfg, "head")
        
        logger.info("✓ Migrations completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
