#!/usr/bin/env python3
"""
Main entry point for FastAPI deployment on Replit.
This file provides the standard 'main.py' entry point that Replit expects.
"""

from run_production import app

# This is the standard FastAPI app instance that deployment systems expect
# The 'app' variable is imported from our main production file
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")