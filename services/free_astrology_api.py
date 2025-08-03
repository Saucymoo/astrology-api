"""
Free Astrology API service for accurate Whole Sign house calculations.
Uses https://freeastrologyapi.com for real astronomical data.
"""

import httpx
import logging
from typing import Dict, Any, List
from datetime import datetime
from models import BirthInfoRequest

logger = logging.getLogger(__name__)

class FreeAstrologyAPIService:
    """Service for interacting with freeastrologyapi.com"""
    
    def __init__(self):
        self.base_url = "https://freeastrologyapi.com"
        self.timeout = 30.0
        
    async def get_houses_data(self, birth_info: BirthInfoRequest) -> Dict[str, Any]:
        """
        Get house data from Free Astrology API using Whole Sign system.
        
        Args:
            birth_info: Birth information with coordinates
            
        Returns:
            Complete house and planetary data
        """
        try:
            # Prepare request data
            request_data = {
                "date": birth_info.date,
                "time": birth_info.time,
                "latitude": birth_info.latitude,
                "longitude": birth_info.longitude,
                "timezone": birth_info.timezone,
                "house_system": "Whole Signs"
            }
            
            logger.info(f"Calling Free Astrology API with Whole Signs system")
            logger.info(f"Request data: {request_data}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Use the Western Astrology > Houses endpoint
                response = await client.post(
                    f"{self.base_url}/api/houses",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                logger.info(f"API Response status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info("Successfully received houses data from Free Astrology API")
                    return data
                else:
                    logger.error(f"API error: {response.status_code} - {response.text}")
                    raise Exception(f"API request failed: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Free Astrology API request failed: {str(e)}")
            raise Exception(f"Failed to get astrology data: {str(e)}")
    
    def format_api_response(self, api_data: Dict[str, Any], birth_info: BirthInfoRequest) -> Dict[str, Any]:
        """
        Format the API response into our standard format.
        
        Args:
            api_data: Raw API response
            birth_info: Original birth information
            
        Returns:
            Formatted chart data
        """
        try:
            # Extract planets data
            planets = api_data.get('planets', {})
            houses = api_data.get('houses', {})
            
            # Create placements array
            placements = []
            
            # List of planets to include
            planet_names = [
                'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 
                'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto',
                'North Node', 'South Node', 'Chiron'
            ]
            
            for planet_name in planet_names:
                if planet_name in planets:
                    planet_data = planets[planet_name]
                    
                    placement = {
                        "planet": planet_name,
                        "sign": planet_data.get('sign', 'Unknown'),
                        "house": planet_data.get('house', 1),
                        "degree": planet_data.get('degree', 0.0),
                        "exactDegree": self._format_exact_degree(planet_data.get('degree', 0.0)),
                        "retrograde": planet_data.get('retrograde', False)
                    }
                    placements.append(placement)
            
            # Get ascendant and midheaven
            ascendant = api_data.get('ascendant', {})
            midheaven = api_data.get('midheaven', {})
            
            # Format response
            response = {
                "name": birth_info.name,
                "birthDate": birth_info.date,
                "birthTime": birth_info.time,
                "location": birth_info.location,
                "coordinates": {
                    "latitude": birth_info.latitude,
                    "longitude": birth_info.longitude,
                    "timezone": birth_info.timezone
                },
                "houseSystem": "Whole Signs",
                "risingSign": ascendant.get('sign', 'Unknown'),
                "sunSign": next((p['sign'] for p in placements if p['planet'] == 'Sun'), 'Unknown'),
                "moonSign": next((p['sign'] for p in placements if p['planet'] == 'Moon'), 'Unknown'),
                "ascendant": {
                    "sign": ascendant.get('sign', 'Unknown'),
                    "degree": ascendant.get('degree', 0.0),
                    "exactDegree": self._format_exact_degree(ascendant.get('degree', 0.0))
                },
                "midheaven": {
                    "sign": midheaven.get('sign', 'Unknown'),
                    "degree": midheaven.get('degree', 0.0),
                    "exactDegree": self._format_exact_degree(midheaven.get('degree', 0.0))
                },
                "placements": placements,
                "generatedAt": datetime.now().isoformat(),
                "source": "Free Astrology API"
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Response formatting failed: {str(e)}")
            raise Exception(f"Failed to format API response: {str(e)}")
    
    def _format_exact_degree(self, degree: float) -> str:
        """Format a decimal degree to degrees, minutes, seconds format."""
        deg = int(degree)
        min_val = int((degree % 1) * 60)
        sec = int(((degree % 1) * 60 % 1) * 60)
        return f"{deg}°{min_val:02d}'{sec:02d}\""