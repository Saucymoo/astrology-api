"""
Production runner for the Astrology API.

This script configures the API for production use with real external APIs.
Set ENVIRONMENT=production to use real astrology services.
"""

import os
import uvicorn
from main import app
from config import get_config, use_real_apis

def setup_production():
    """Configure the application for production use."""
    
    # Set environment
    os.environ["ENVIRONMENT"] = "production"
    
    # Import real services for production
    if use_real_apis():
        # Replace mock service with real astrology service
        from services.astrology_service import AstrologyService
        from main import astrology_service
        
        # Update the service instance
        app.dependency_overrides = {}
        print("✓ Configured to use real astrology APIs")
    else:
        print("ℹ Using mock services (set ENVIRONMENT=production for real APIs)")

if __name__ == "__main__":
    setup_production()
    config = get_config()
    
    print(f"Starting Astrology API in {os.getenv('ENVIRONMENT', 'development')} mode...")
    print(f"Server will run on {config['host']}:{config['port']}")
    print(f"Documentation available at: http://{config['host']}:{config['port']}/docs")
    
    uvicorn.run(
        "main:app",
        host=config["host"],
        port=config["port"],
        reload=config["reload"],
        log_level=config["log_level"]
    )