#!/usr/bin/env python3
"""
Production server startup for the Astrology Chart API.
"""

import uvicorn
import logging
from main import app

# Configure production logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting Astrology Chart API server...")
    logger.info("API Documentation available at: http://localhost:8000/docs")
    logger.info("Health check available at: http://localhost:8000/health")
    logger.info("Main endpoint: POST http://localhost:8000/generate-chart")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False  # Production mode
    )