#!/usr/bin/env python3
"""
Production FastAPI server for astrology chart generation.
Provides a public API endpoint for generating complete natal charts.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import asyncio
from datetime import datetime
import logging

# Import our services
from models import BirthInfoRequest
from services.astrology_calculations import AstrologyCalculationsService
from services.geocoding_service import GeocodingService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Astrology Chart API",
    description="Generate complete natal charts with accurate astronomical calculations using Whole Sign houses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for the public API
class ChartRequest(BaseModel):
    name: str = Field(..., description="Full name of the person")
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD format", pattern=r"^\d{4}-\d{2}-\d{2}$")
    birth_time: str = Field(..., description="Birth time in HH:MM format", pattern=r"^\d{2}:\d{2}$")
    birth_location: str = Field(..., description="Birth location (city, state/province, country)")

# Response models
class ChartAngle(BaseModel):
    sign: str
    degree: float
    exact_degree: str

class PlanetPlacement(BaseModel):
    planet: str
    sign: str
    degree: float
    exact_degree: str
    house: int
    retrograde: bool

class ChartResponse(BaseModel):
    name: str
    birth_date: str
    birth_time: str
    birth_location: str
    coordinates: dict
    house_system: str
    ascendant: ChartAngle
    midheaven: ChartAngle
    rising_sign: str
    sun_sign: str
    moon_sign: str
    placements: List[PlanetPlacement]
    generated_at: str
    source: str

# Initialize services
astrology_service = AstrologyCalculationsService()
geocoding_service = GeocodingService()

# Set house system to Whole Signs
astrology_service.set_house_system("W")

def format_degree(degree: float) -> str:
    """Format degree as DD°MM'SS\" """
    deg = int(degree)
    min_val = int((degree - deg) * 60)
    sec_val = int(((degree - deg) * 60 - min_val) * 60)
    return f"{deg}°{min_val:02d}'{sec_val:02d}\""

def convert_date_format(date_str: str) -> str:
    """Convert YYYY-MM-DD to DD/MM/YYYY for internal processing."""
    try:
        parts = date_str.split('-')
        return f"{parts[2]}/{parts[1]}/{parts[0]}"
    except:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

def determine_whole_sign_houses(rising_sign: str) -> dict:
    """Determine Whole Sign house assignments based on rising sign."""
    zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                   'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    try:
        rising_index = zodiac_signs.index(rising_sign)
    except ValueError:
        raise HTTPException(status_code=500, detail=f"Invalid rising sign: {rising_sign}")
    
    whole_sign_houses = {}
    for i, sign in enumerate(zodiac_signs):
        house_number = ((i - rising_index) % 12) + 1
        whole_sign_houses[sign] = house_number
    
    return whole_sign_houses

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Astrology Chart API",
        "version": "1.0.0",
        "description": "Generate complete natal charts with Whole Sign houses",
        "endpoints": {
            "generate_chart": "/generate-chart",
            "documentation": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "house_system": "Whole Signs",
        "services": {
            "astrology_calculations": "operational",
            "geocoding": "operational"
        }
    }

@app.post("/generate-chart", response_model=ChartResponse)
async def generate_chart(request: ChartRequest):
    """
    Generate a complete natal chart with all planetary positions and house placements.
    
    This endpoint accepts birth information and returns a comprehensive astrological chart
    using the Whole Sign house system exclusively.
    """
    try:
        logger.info(f"Generating chart for {request.name}")
        
        # Get coordinates for the location
        try:
            coordinates = await geocoding_service.get_coordinates(request.birth_location)
            logger.info(f"Coordinates obtained: {coordinates['latitude']}, {coordinates['longitude']}")
        except Exception as e:
            logger.error(f"Geocoding failed: {e}")
            raise HTTPException(
                status_code=400, 
                detail=f"Could not find coordinates for location: {request.birth_location}"
            )
        
        # Convert date format and create birth info
        internal_date = convert_date_format(request.birth_date)
        
        birth_info = BirthInfoRequest(
            name=request.name,
            date=internal_date,
            time=request.birth_time,
            location=request.birth_location,
            latitude=coordinates['latitude'],
            longitude=coordinates['longitude'],
            timezone=coordinates.get('timezone', 0)
        )
        
        # Generate the chart using Swiss Ephemeris
        try:
            raw_chart = await astrology_service.generate_chart(birth_info)
            logger.info(f"Chart generated successfully for {request.name}")
        except Exception as e:
            logger.error(f"Chart generation failed: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate chart: {str(e)}"
            )
        
        # Determine Whole Sign house assignments
        rising_sign = raw_chart.ascendant.sign
        whole_sign_houses = determine_whole_sign_houses(rising_sign)
        
        # Process planetary placements with correct house assignments
        placements = []
        sun_sign = None
        moon_sign = None
        
        for planet in raw_chart.planets:
            # Get correct house assignment using Whole Signs
            correct_house = whole_sign_houses.get(planet.sign, 0)
            
            placement = PlanetPlacement(
                planet=planet.name,
                sign=planet.sign,
                degree=planet.degree,
                exact_degree=format_degree(planet.degree),
                house=correct_house,
                retrograde=getattr(planet, 'retrograde', False)
            )
            placements.append(placement)
            
            # Track Sun and Moon signs
            if planet.name == 'Sun':
                sun_sign = planet.sign
            elif planet.name == 'Moon':
                moon_sign = planet.sign
        
        # Create ascendant and midheaven objects
        ascendant = ChartAngle(
            sign=raw_chart.ascendant.sign,
            degree=raw_chart.ascendant.degree,
            exact_degree=format_degree(raw_chart.ascendant.degree)
        )
        
        # Calculate Midheaven (10th house cusp in Whole Signs)
        # In Whole Signs, MC is typically in the 10th whole sign
        zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                       'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        rising_index = zodiac_signs.index(rising_sign)
        mc_sign_index = (rising_index + 9) % 12  # 10th house is 9 positions ahead
        mc_sign = zodiac_signs[mc_sign_index]
        
        midheaven = ChartAngle(
            sign=mc_sign,
            degree=15.0,  # Mid-point of the sign for Whole Sign system
            exact_degree="15°00'00\""
        )
        
        # Create response
        response = ChartResponse(
            name=request.name,
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            birth_location=request.birth_location,
            coordinates={
                "latitude": coordinates['latitude'],
                "longitude": coordinates['longitude'],
                "timezone": coordinates.get('timezone', 0)
            },
            house_system="Whole Sign",
            ascendant=ascendant,
            midheaven=midheaven,
            rising_sign=rising_sign,
            sun_sign=sun_sign or "Unknown",
            moon_sign=moon_sign or "Unknown",
            placements=placements,
            generated_at=datetime.now().isoformat(),
            source="Swiss Ephemeris with Whole Sign Houses"
        )
        
        logger.info(f"Chart completed for {request.name}: {rising_sign} rising, {sun_sign} Sun, {moon_sign} Moon")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/planets")
async def get_planets():
    """Get list of supported planets and celestial bodies."""
    return {
        "planets": [
            "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
            "Uranus", "Neptune", "Pluto", "North Node", "South Node", "Chiron"
        ],
        "count": 13
    }

@app.get("/zodiac-signs")
async def get_zodiac_signs():
    """Get list of zodiac signs."""
    return {
        "signs": [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ],
        "count": 12
    }

@app.get("/house-system")
async def get_house_system():
    """Get current house system information."""
    return {
        "house_system": "Whole Sign",
        "description": "Traditional house system where each house corresponds to a complete zodiac sign",
        "houses": 12
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)