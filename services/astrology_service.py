"""
Astrology service for generating birth charts using the Free Astrology API.

This service handles communication with external astrology APIs and 
processes the data into standardized formats.
"""

import requests
import logging
import os
from typing import Dict, List, Any
from datetime import datetime

from models import BirthInfoRequest, AstrologyResponse, Planet, House, Ascendant

logger = logging.getLogger(__name__)


class AstrologyService:
    """Service for generating astrology charts."""
    
    def __init__(self):
        self.base_url = "https://api.freeastrologyapi.com/api/v1"
        self.timeout = 30
        self.api_key = os.getenv("FREE_ASTROLOGY_API_KEY")
        
        if not self.api_key:
            logger.warning("FREE_ASTROLOGY_API_KEY not found in environment variables")
        
        # House system configuration - CRITICAL FOR ASTROLOGICAL ACCURACY
        self.house_system = "W"  # Whole Sign Houses
        # Available options:
        # "P" = Placidus (default in many systems)
        # "K" = Koch
        # "O" = Porphyrius
        # "R" = Regiomontanus
        # "C" = Campanus
        # "A" = Equal Houses
        # "V" = Vehlow Equal Houses
        # "W" = Whole Sign Houses
        # "X" = Meridian Houses
        # "H" = Azimuthal
        # "T" = Topocentric
        # "B" = Alcabitius
        # "M" = Morinus
        
        # Zodiac sign mapping
        self.zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
    
    async def generate_chart(self, birth_info: BirthInfoRequest) -> AstrologyResponse:
        """
        Generate a complete astrology chart from birth information.
        
        Args:
            birth_info: Birth details including date, time, and location
            
        Returns:
            AstrologyResponse: Complete chart with planets, houses, and ascendant
            
        Raises:
            Exception: If API call fails or data processing fails
        """
        try:
            # Call the birth chart API
            raw_data = await self._call_birth_chart_api(birth_info)
            
            # Process the raw API response
            chart_data = self._process_chart_data(raw_data)
            
            # Create response model
            response = AstrologyResponse(
                success=True,
                name=birth_info.name,
                birth_info=birth_info,
                planets=chart_data["planets"],
                houses=chart_data["houses"],
                ascendant=chart_data["ascendant"],
                generated_at=datetime.now()
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Chart generation failed: {str(e)}")
            raise Exception(f"Failed to generate astrology chart: {str(e)}")
    
    async def _call_birth_chart_api(self, birth_info: BirthInfoRequest) -> Dict[str, Any]:
        """
        Call the Free Astrology API to get birth chart data.
        
        Args:
            birth_info: Birth information
            
        Returns:
            Raw API response data
        """
        try:
            # Parse date and time
            date_parts = birth_info.date.split('-')
            time_parts = birth_info.time.split(':')
            
            year = int(date_parts[0])
            month = int(date_parts[1])
            day = int(date_parts[2])
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            
            # Prepare API request payload with Whole Sign house system
            payload = {
                "day": day,
                "month": month,
                "year": year,
                "hour": hour,
                "min": minute,
                "lat": birth_info.latitude,
                "lon": birth_info.longitude,
                "tzone": birth_info.timezone or 0,
                "house_system": self.house_system  # "W" for Whole Sign Houses
            }
            
            logger.info(f"Calling Free Astrology API with payload: {payload}")
            
            # Make API request with authentication
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Astrology-Chart-API/1.0"
            }
            
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.post(
                f"{self.base_url}/birth-chart",
                json=payload,
                timeout=self.timeout,
                headers=headers
            )
            
            if not response.ok:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
            
            data = response.json()
            logger.info("Successfully received data from Free Astrology API")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise Exception(f"Failed to call astrology API: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in API call: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")
    
    def _process_chart_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw API data into standardized format.
        
        Args:
            raw_data: Raw API response
            
        Returns:
            Processed chart data with planets, houses, and ascendant
        """
        try:
            logger.info("Processing chart data...")
            
            # Extract planets
            planets = []
            if "planets" in raw_data:
                for planet_data in raw_data["planets"]:
                    planet = Planet(
                        name=planet_data.get("name", "Unknown"),
                        sign=planet_data.get("sign", self._get_sign_name(planet_data.get("sign_num", 1))),
                        sign_num=planet_data.get("sign_num", 1),
                        degree=float(planet_data.get("degree", 0)),
                        house=int(planet_data.get("house", 1)),
                        retro=planet_data.get("retro", False)
                    )
                    planets.append(planet)
            
            # Extract houses
            houses = []
            if "houses" in raw_data:
                for house_data in raw_data["houses"]:
                    house = House(
                        house=int(house_data.get("house", 1)),
                        sign=house_data.get("sign", self._get_sign_name(house_data.get("sign_num", 1))),
                        sign_num=house_data.get("sign_num", 1),
                        degree=float(house_data.get("degree", 0))
                    )
                    houses.append(house)
            
            # Extract ascendant
            ascendant_data = raw_data.get("ascendant", {})
            ascendant = Ascendant(
                sign=ascendant_data.get("sign", self._get_sign_name(ascendant_data.get("sign_num", 1))),
                degree=float(ascendant_data.get("degree", 0))
            )
            
            logger.info(f"Processed {len(planets)} planets, {len(houses)} houses")
            
            return {
                "planets": planets,
                "houses": houses,
                "ascendant": ascendant
            }
            
        except Exception as e:
            logger.error(f"Data processing failed: {str(e)}")
            raise Exception(f"Failed to process chart data: {str(e)}")
    
    def _get_sign_name(self, sign_num: int) -> str:
        """
        Get zodiac sign name from sign number.
        
        Args:
            sign_num: Sign number (1-12)
            
        Returns:
            Zodiac sign name
        """
        if 1 <= sign_num <= 12:
                return self.zodiac_signs[sign_num - 1]
        return "Unknown"
    
    def set_house_system(self, house_system: str) -> None:
        """Change the house system used for calculations."""
        valid_systems = ["P", "K", "O", "R", "C", "A", "V", "W", "X", "H", "T", "B", "M"]
        if house_system not in valid_systems:
            raise ValueError(f"Invalid house system '{house_system}'. Valid options: {valid_systems}")
        
        self.house_system = house_system
        logger.info(f"House system changed to: {house_system}")
    
    def get_house_system(self) -> str:
        """Get current house system setting."""
        return self.house_system
    
    def get_supported_planets(self) -> List[str]:
        """Get list of supported planets and astrological points."""
        return [
            "Sun", "Moon", "Mercury", "Venus", "Mars",
            "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto",
            "Chiron", "North Node", "South Node"
        ]
    
    def get_zodiac_signs(self) -> List[str]:
        """Get list of zodiac signs."""
        return self.zodiac_signs.copy()
    
    def set_house_system(self, house_system: str) -> None:
        """
        Change the house system used for calculations.
        
        Args:
            house_system: House system code (e.g., "W" for Whole Sign, "P" for Placidus)
        """
        valid_systems = ["P", "K", "O", "R", "C", "A", "V", "W", "X", "H", "T", "B", "M"]
        if house_system not in valid_systems:
            raise ValueError(f"Invalid house system '{house_system}'. Valid options: {valid_systems}")
        
        self.house_system = house_system
        logger.info(f"House system changed to: {house_system}")
    
    def get_house_system(self) -> str:
        """Get current house system setting."""
        return self.house_system
    
    def get_available_house_systems(self) -> Dict[str, str]:
        """Get all available house systems with descriptions."""
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