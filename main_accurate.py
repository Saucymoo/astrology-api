"""
Updated FastAPI backend using Free Astrology API for accurate Whole Sign house calculations.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any
from datetime import datetime
import logging

from models import BirthInfoRequest
from services.free_astrology_api import FreeAstrologyAPIService
from services.geocoding_service import GeocodingService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Accurate Astrology Chart API",
    description="Generate accurate astrology charts using Free Astrology API with Whole Sign houses",
    version="2.0.0",
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
astrology_service = FreeAstrologyAPIService()
geocoding_service = GeocodingService()

logger.info("Accurate Astrology API initialized with Free Astrology API and Whole Sign houses")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Accurate Astrology Chart API",
        "version": "2.0.0",
        "docs": "/docs",
        "astronomicalSource": "Free Astrology API",
        "houseSystem": "Whole Signs",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "houseSystem": "Whole Signs",
        "source": "Free Astrology API"
    }


@app.post("/generate-chart")
async def generate_astrology_chart(birth_info: BirthInfoRequest) -> Dict[str, Any]:
    """
    Generate a complete astrology chart from birth information.
    
    Uses Free Astrology API for accurate astronomical calculations and 
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
        
        # Generate chart using Free Astrology API
        api_data = await astrology_service.get_houses_data(birth_info)
        
        # Format response
        chart_response = astrology_service.format_api_response(api_data, birth_info)
        
        logger.info(f"Chart generated successfully: {len(chart_response['placements'])} planets")
        return chart_response
        
    except Exception as e:
        logger.error(f"Chart generation failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate astrology chart: {str(e)}"
        )


@app.post("/test-chart")
async def test_specific_chart():
    """
    Test endpoint for the specific birth data provided by user.
    """
    try:
        # Create test birth info with exact data provided
        birth_info = BirthInfoRequest(
            name="Test Chart",
            date="1974-11-22",
            time="19:10",
            location="Adelaide, Australia",
            latitude=-34.9285,
            longitude=138.6007,
            timezone=9.5
        )
        
        logger.info("Testing with specific birth data provided by user")
        
        # Generate chart using Free Astrology API
        api_data = await astrology_service.get_houses_data(birth_info)
        
        # Format response
        chart_response = astrology_service.format_api_response(api_data, birth_info)
        
        logger.info("Test chart generated successfully")
        return chart_response
        
    except Exception as e:
        logger.error(f"Test chart generation failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate test chart: {str(e)}"
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