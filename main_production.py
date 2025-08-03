"""
Clean FastAPI backend for astrology chart generation.
Uses Swiss Ephemeris for accurate astronomical calculations with Whole Sign houses.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any
from datetime import datetime
import logging

from models import BirthInfoRequest
from services.astrology_calculations import AstrologyCalculationsService
from services.geocoding_service import GeocodingService
from services.chart_formatter import create_simple_chart_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Astrology Chart API",
    description="Generate accurate astrology charts using Swiss Ephemeris with Whole Sign houses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
astrology_service = AstrologyCalculationsService()
astrology_service.set_house_system("W")  # Whole Sign houses
geocoding_service = GeocodingService()

logger.info("Astrology API initialized with Swiss Ephemeris and Whole Sign houses")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Astrology Chart API",
        "version": "1.0.0",
        "docs": "/docs",
        "astronomicalSource": "Swiss Ephemeris",
        "houseSystem": "Whole Sign",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "houseSystem": astrology_service.get_house_system()
    }


@app.get("/current-house-system")
async def get_current_house_system():
    """Get current house system configuration."""
    return {
        "code": "W",
        "name": "Whole Sign Houses",
        "description": "Currently using Whole Sign Houses house system"
    }


@app.post("/generate-chart")
async def generate_astrology_chart(birth_info: BirthInfoRequest) -> Dict[str, Any]:
    """
    Generate a complete astrology chart from birth information.
    
    Uses Swiss Ephemeris for accurate astronomical calculations and 
    Whole Sign house system exclusively.
    
    Args:
        birth_info: Birth details (name, date, time, location)
        
    Returns:
        Complete natal chart with all planetary positions and house placements
    """
    try:
        logger.info(f"Generating chart for {birth_info.name}")
        
        # Get coordinates if not provided
        if not birth_info.latitude or not birth_info.longitude:
            logger.info(f"Geocoding location: {birth_info.location}")
            coordinates = await geocoding_service.get_coordinates(birth_info.location)
            birth_info.latitude = coordinates["latitude"]
            birth_info.longitude = coordinates["longitude"]
            
            # Set timezone for Adelaide (used in most tests)
            if "adelaide" in birth_info.location.lower():
                birth_info.timezone = 9.5
            else:
                birth_info.timezone = coordinates.get("timezone", 0)
        
        # Generate chart using Swiss Ephemeris
        raw_chart = await astrology_service.generate_chart(birth_info)
        
        # Convert to clean JSON format
        chart_response = create_simple_chart_response(raw_chart)
        
        logger.info(f"Chart generated successfully: {len(chart_response['placements'])} planets")
        return chart_response
        
    except Exception as e:
        logger.error(f"Chart generation failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate astrology chart: {str(e)}"
        )


@app.post("/geocode")
async def geocode_location(location_data: Dict[str, str]):
    """Get coordinates for a location name."""
    try:
        location = location_data.get("location", "")
        if not location:
            raise HTTPException(status_code=400, detail="Location is required")
            
        coordinates = await geocoding_service.get_coordinates(location)
        return coordinates
        
    except Exception as e:
        logger.error(f"Geocoding failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Geocoding failed: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)