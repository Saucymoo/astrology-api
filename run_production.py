#!/usr/bin/env python3
"""
Simple production server runner for the Astrology Chart API.
"""

import asyncio
import json
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uvicorn


# Simple request/response models
class SimpleChartRequest(BaseModel):
    name: str
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    birth_location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone_name: Optional[str] = None


class SimpleChartResponse(BaseModel):
    name: str
    birth_date: str
    birth_time: str
    birth_location: str
    house_system: str
    ascendant: dict
    midheaven: dict
    rising_sign: str
    sun_sign: str
    moon_sign: str
    placements: list
    generated_at: str
    source: str


# Create FastAPI app
app = FastAPI(
    title="Astrology Chart API",
    description="Generate complete natal charts with Whole Sign houses",
    version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Astrology Chart API",
        "version": "1.0.0",
        "endpoints": {
            "generate_chart": "/generate-chart",
            "health": "/health",
            "docs": "/docs"
        },
        "status": "active"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "house_system": "Whole Sign"
    }


@app.post("/generate-chart")
async def generate_chart(request: SimpleChartRequest):
    """Generate natal chart - using our proven accurate calculations."""

    try:
        # Import our working services
        from models import BirthInfoRequest
        from services.astrology_calculations import AstrologyCalculationsService
        from services.geocoding_service import GeocodingService

        # Initialize services
        astrology_service = AstrologyCalculationsService()
        geocoding_service = GeocodingService()
        astrology_service.set_house_system("W")  # Whole Signs

        # Convert date format (YYYY-MM-DD to DD/MM/YYYY)
        date_parts = request.birth_date.split('-')
        internal_date = f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}"

        # Get coordinates
        coordinates = await geocoding_service.get_coordinates(
            request.birth_location)

        # Create birth info
        birth_info = BirthInfoRequest(
            name=request.name,
            date=internal_date,
            time=request.birth_time,
            location=request.birth_location,
            latitude=coordinates['latitude'],
            longitude=coordinates['longitude'],
            timezone=coordinates.get('timezone', 0),
            timezone_name=request.timezone_name
            or coordinates.get('timezone_name', "UTC")
            # ← Use directly from the request
        )

        # Generate chart
        raw_chart = await astrology_service.generate_chart(birth_info)

        # Process results with Whole Sign houses
        rising_sign = raw_chart.ascendant.sign

        # Calculate Whole Sign house assignments
        zodiac_signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra',
            'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        rising_index = zodiac_signs.index(rising_sign)

        whole_sign_houses = {}
        for i, sign in enumerate(zodiac_signs):
            house_number = ((i - rising_index) % 12) + 1
            whole_sign_houses[sign] = house_number

        # Process planets
        placements = []
        sun_sign = None
        moon_sign = None

        for planet in raw_chart.planets:
            house = whole_sign_houses.get(planet.sign, 0)
            degree = planet.degree

            placement = {
                "planet": planet.name,
                "sign": planet.sign,
                "degree": degree,
                "exact_degree":
                f"{int(degree)}°{int((degree % 1) * 60):02d}'{int(((degree % 1) * 60 % 1) * 60):02d}\"",
                "house": house,
                "retrograde": getattr(planet, 'retro', False)
            }
            placements.append(placement)

            if planet.name == 'Sun':
                sun_sign = planet.sign
            elif planet.name == 'Moon':
                moon_sign = planet.sign

        # Create response
        asc_degree = raw_chart.ascendant.degree
        mc_sign = raw_chart.midheaven.sign
        mc_degree = raw_chart.midheaven.degree

        # Determine which Whole Sign house the Midheaven falls in
        mc_house = whole_sign_houses.get(mc_sign, 0)

        response = {
            "name": request.name,
            "birth_date": request.birth_date,
            "birth_time": request.birth_time,
            "birth_location": request.birth_location,
            "coordinates": {
                "latitude": coordinates['latitude'],
                "longitude": coordinates['longitude'],
                "timezone": coordinates.get('timezone', 0)
            },
            "house_system": "Whole Sign",
            "ascendant": {
                "sign":
                rising_sign,
                "degree":
                asc_degree,
                "exact_degree":
                f"{int(asc_degree)}°{int((asc_degree % 1) * 60):02d}'{int(((asc_degree % 1) * 60 % 1) * 60):02d}\""
            },
            "midheaven": {
                "sign":
                mc_sign,
                "degree":
                mc_degree,
                "house":
                mc_house,
                "exact_degree":
                f"{int(mc_degree)}°{int((mc_degree % 1) * 60):02d}'{int(((mc_degree % 1) * 60 % 1) * 60):02d}\""
            },
            "rising_sign": rising_sign,
            "sun_sign": sun_sign or "Unknown",
            "moon_sign": moon_sign or "Unknown",
            "placements": placements,
            "generated_at": datetime.now().isoformat(),
            "source": "Swiss Ephemeris with Whole Sign Houses"
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Chart generation failed: {str(e)}")


if __name__ == "__main__":
    print("Starting Astrology Chart API on port 8000...")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
