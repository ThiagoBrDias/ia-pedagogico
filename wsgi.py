"""
WSGI entry point for Umbler deployment
"""
import os
import sys

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from app import app

# This is the WSGI application that Umbler will use
application = app

if __name__ == "__main__":
    # For local testing
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
