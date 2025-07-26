"""
FastAPI backend for astrology chart generation.

This API accepts birth information (date, time, location) and returns 
astrological placements including planetary positions, houses, and key signs.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional, List, Dict, Any
import requests
from datetime import datetime
import logging

from models import (
    BirthInfoRequest, 
    AstrologyResponse, 
    Planet, 
    House, 
    Ascendant,
    ErrorResponse
)
from models_enhanced import ChartResponse, PlacementInfo
from services.mock_astrology_service import MockAstrologyService
from services.geocoding_service import GeocodingService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Astrology Chart API",
    description="Generate personalized astrology charts from birth information",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
astrology_service = MockAstrologyService()
geocoding_service = GeocodingService()


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Astrology Chart API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }


@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/generate-chart", response_model=ChartResponse)
async def generate_astrology_chart(birth_info: BirthInfoRequest):
    """
    Generate an astrology chart from birth information.
    
    Returns data in clean JSON format with risingSign, sunSign, moonSign, 
    midheaven, and detailed placements array using Whole Sign houses.
    
    Args:
        birth_info: Birth details including name, date, time, and location
        
    Returns:
        ChartResponse: Clean JSON with key placements and house information
                          
    Raises:
        HTTPException: If chart generation fails
    """
    try:
        logger.info(f"Generating chart for {birth_info.name} born {birth_info.date} {birth_info.time} in {birth_info.location}")
        
        # Get coordinates if not provided
        if not birth_info.latitude or not birth_info.longitude:
            logger.info(f"Geocoding location: {birth_info.location}")
            coordinates = await geocoding_service.get_coordinates(birth_info.location)
            birth_info.latitude = coordinates["latitude"]
            birth_info.longitude = coordinates["longitude"]
            if not birth_info.timezone:
                birth_info.timezone = coordinates.get("timezone", 0)
        
        # Generate astrology chart
        logger.info("Calling astrology service...")
        raw_chart = await astrology_service.generate_chart(birth_info)
        
        # Convert to user's preferred format
        chart_response = _convert_to_chart_response(raw_chart)
        
        logger.info("Chart generated successfully")
        return chart_response
        
    except Exception as e:
        logger.error(f"Chart generation failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate astrology chart: {str(e)}"
        )


def _convert_to_chart_response(raw_chart: AstrologyResponse) -> ChartResponse:
    """Convert internal chart format to user's preferred response format."""
    
    # Find key planets
    planets = raw_chart.planets
    sun = next((p for p in planets if p.name == "Sun"), None)
    moon = next((p for p in planets if p.name == "Moon"), None)
    
    # Get Midheaven (10th house cusp)
    tenth_house = next((h for h in raw_chart.houses if h.house == 10), None)
    midheaven_sign = tenth_house.sign if tenth_house else "Unknown"
    
    # Create placements array
    placements = [
        PlacementInfo(
            planet=planet.name,
            sign=planet.sign,
            house=planet.house,
            degree=planet.degree,
            retrograde=planet.retro or False
        )
        for planet in planets
    ]
    
    return ChartResponse(
        risingSign=raw_chart.ascendant.sign,
        sunSign=sun.sign if sun else "Unknown",
        moonSign=moon.sign if moon else "Unknown", 
        midheaven=midheaven_sign,
        placements=placements
    )


@app.post("/geocode", response_model=Dict[str, Any])
async def geocode_location(location: Dict[str, str]):
    """
    Get coordinates for a location name.
    
    Args:
        location: Dictionary with 'location' key containing location name
        
    Returns:
        Dictionary with latitude, longitude, and estimated timezone
    """
    try:
        location_name = location.get("location")
        if not location_name:
            raise HTTPException(status_code=400, detail="Location name is required")
            
        coordinates = await geocoding_service.get_coordinates(location_name)
        return coordinates
        
    except Exception as e:
        logger.error(f"Geocoding failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to geocode location: {str(e)}"
        )


@app.get("/planets", response_model=List[str])
async def get_supported_planets():
    """Get list of supported planets and celestial bodies."""
    return [
        "Sun", "Moon", "Mercury", "Venus", "Mars", 
        "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto",
        "North Node", "South Node", "Chiron"
    ]


@app.get("/zodiac-signs", response_model=List[str])
async def get_zodiac_signs():
    """Get list of zodiac signs."""
    return [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]


@app.get("/house-systems", response_model=Dict[str, str])
async def get_house_systems():
    """Get available house systems with descriptions."""
    return {
        "P": "Placidus",
        "K": "Koch", 
        "O": "Porphyrius",
        "R": "Regiomontanus",
        "C": "Campanus",
        "A": "Equal Houses",
        "V": "Vehlow Equal Houses", 
        "W": "Whole Sign Houses",
        "X": "Meridian Houses",
        "H": "Azimuthal",
        "T": "Topocentric",
        "B": "Alcabitius",
        "M": "Morinus"
    }


@app.get("/current-house-system", response_model=Dict[str, str])
async def get_current_house_system():
    """Get currently configured house system."""
    current = astrology_service.get_house_system()
    systems = {
        "P": "Placidus", "K": "Koch", "O": "Porphyrius", "R": "Regiomontanus",
        "C": "Campanus", "A": "Equal Houses", "V": "Vehlow Equal Houses", 
        "W": "Whole Sign Houses", "X": "Meridian Houses", "H": "Azimuthal",
        "T": "Topocentric", "B": "Alcabitius", "M": "Morinus"
    }
    return {
        "code": current,
        "name": systems.get(current, "Unknown"),
        "description": f"Currently using {systems.get(current, 'Unknown')} house system"
    }


@app.post("/set-house-system", response_model=Dict[str, str])
async def set_house_system(request: Dict[str, str]):
    """
    Change the house system used for chart calculations.
    
    Args:
        request: Dictionary with 'house_system' key (e.g., {"house_system": "W"})
    
    Returns:
        Confirmation of the change
    """
    try:
        house_system = request.get("house_system")
        if not house_system:
            raise HTTPException(status_code=400, detail="house_system parameter is required")
        
        astrology_service.set_house_system(house_system)
        
        systems = {
            "P": "Placidus", "K": "Koch", "O": "Porphyrius", "R": "Regiomontanus",
            "C": "Campanus", "A": "Equal Houses", "V": "Vehlow Equal Houses", 
            "W": "Whole Sign Houses", "X": "Meridian Houses", "H": "Azimuthal",
            "T": "Topocentric", "B": "Alcabitius", "M": "Morinus"
        }
        
        return {
            "success": "true",
            "message": f"House system changed to {systems.get(house_system, 'Unknown')}",
            "code": house_system,
            "name": systems.get(house_system, "Unknown")
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set house system: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )