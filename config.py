"""
Configuration settings for the Astrology API.

Use this file to switch between development and production settings.
"""

import os
from typing import Dict, Any

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, production

# API Configuration
API_CONFIG: Dict[str, Any] = {
    "development": {
        "use_mock_service": True,
        "debug": True,
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,
        "log_level": "debug"
    },
    "production": {
        "use_mock_service": False,
        "debug": False,
        "host": "0.0.0.0", 
        "port": int(os.getenv("PORT", 8000)),
        "reload": False,
        "log_level": "info"
    }
}

# Get current configuration
CURRENT_CONFIG = API_CONFIG.get(ENVIRONMENT, API_CONFIG["development"])

# External API URLs
FREE_ASTROLOGY_API_BASE = "https://api.freeastrologyapi.com/api/v1"
NOMINATIM_API_BASE = "https://nominatim.openstreetmap.org"

# API timeouts
API_TIMEOUT = 30
GEOCODING_TIMEOUT = 10

# CORS settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000", 
    "https://yourdomain.com",  # Replace with your domain
]

# Rate limiting (if implemented)
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 3600  # 1 hour

def get_config() -> Dict[str, Any]:
    """Get current configuration based on environment."""
    return CURRENT_CONFIG

def is_production() -> bool:
    """Check if running in production mode."""
    return ENVIRONMENT == "production"

def use_real_apis() -> bool:
    """Check if real APIs should be used (not mock)."""
    return not CURRENT_CONFIG.get("use_mock_service", True)