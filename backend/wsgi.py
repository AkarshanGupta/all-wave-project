"""
Entry point for Render deployment.
Allows Render to properly load the ASGI app.
"""
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the app
from app.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,
    )
