"""
Root entry point for Render deployment.
Ensures proper module imports and ASGI app export.
"""
import os
import sys

# Ensure app module can be imported
sys.path.insert(0, os.path.dirname(__file__))

# Export the ASGI app for Render
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
