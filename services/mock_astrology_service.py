"""
Mock astrology service for demonstration purposes.

This service provides sample astrology data when external APIs are not accessible.
Replace this with the real astrology_service.py when you have API access.
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
import random

from models import BirthInfoRequest, AstrologyResponse, Planet, House, Ascendant

logger = logging.getLogger(__name__)


class MockAstrologyService:
    """Mock service for generating sample astrology charts."""
    
    def __init__(self):
        # House system configuration - MATCHES REAL SERVICE
        self.house_system = "W"  # Whole Sign Houses
        
        self.zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        self.planets = [
            "Sun", "Moon", "Mercury", "Venus", "Mars",
            "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto",
            "Chiron", "North Node", "South Node"
        ]
    
    async def generate_chart(self, birth_info: BirthInfoRequest) -> AstrologyResponse:
        """
        Generate a mock astrology chart for demonstration.
        
        Args:
            birth_info: Birth details
            
        Returns:
            AstrologyResponse: Sample chart with realistic data
        """
        logger.info(f"Generating mock chart for {birth_info.name}")
        
        # Generate sample planetary positions
        planets = []
        for i, planet_name in enumerate(self.planets):
            # Create realistic but random positions
            sign_num = ((i * 3 + hash(birth_info.name)) % 12) + 1
            sign = self.zodiac_signs[sign_num - 1]
            degree = (hash(planet_name + birth_info.date) % 3000) / 100.0
            house = ((i * 2 + hash(birth_info.time)) % 12) + 1
            retro = hash(planet_name + birth_info.name) % 4 == 0  # 25% chance
            
            planet = Planet(
                name=planet_name,
                sign=sign,
                sign_num=sign_num,
                degree=degree,
                house=house,
                retro=retro
            )
            planets.append(planet)
        
        # Generate house cusps using Whole Sign system
        houses = []
        ascendant_sign_num = (hash(birth_info.name + birth_info.location) % 12) + 1
        ascendant_degree = (hash(birth_info.name + birth_info.time) % 3000) / 100.0
        
        if self.house_system == "W":  # Whole Sign Houses
            # In Whole Sign houses, each house occupies exactly one sign
            # 1st house = rising sign, 2nd house = next sign, etc.
            for house_num in range(1, 13):
                house_sign_num = ((ascendant_sign_num + house_num - 2) % 12) + 1
                sign = self.zodiac_signs[house_sign_num - 1]
                # In Whole Sign, house cusp is always at 0° of the sign
                degree = 0.0
                
                house = House(
                    house=house_num,
                    sign=sign,
                    sign_num=house_sign_num,
                    degree=degree
                )
                houses.append(house)
        else:
            # For other house systems, use variable degrees (mock calculation)
            for house_num in range(1, 13):
                house_sign_num = ((ascendant_sign_num + house_num - 2) % 12) + 1
                sign = self.zodiac_signs[house_sign_num - 1]
                degree = (hash(f"house{house_num}" + birth_info.date) % 3000) / 100.0
                
                house = House(
                    house=house_num,
                    sign=sign,
                    sign_num=house_sign_num,
                    degree=degree
                )
                houses.append(house)
        
        # Generate ascendant (rising sign)
        ascendant = Ascendant(
            sign=self.zodiac_signs[ascendant_sign_num - 1],
            degree=(hash(birth_info.name + birth_info.time) % 3000) / 100.0
        )
        
        # Create response
        response = AstrologyResponse(
            success=True,
            name=birth_info.name,
            birth_info=birth_info,
            planets=planets,
            houses=houses,
            ascendant=ascendant,
            generated_at=datetime.now()
        )
        
        logger.info(f"Mock chart generated with {len(planets)} planets and {len(houses)} houses using {self.house_system} house system")
        return response
    
    def set_house_system(self, house_system: str) -> None:
        """Change the house system used for calculations."""
        valid_systems = ["P", "K", "O", "R", "C", "A", "V", "W", "X", "H", "T", "B", "M"]
        if house_system not in valid_systems:
            raise ValueError(f"Invalid house system '{house_system}'. Valid options: {valid_systems}")
        
        self.house_system = house_system
        logger.info(f"Mock service: House system changed to: {house_system}")
    
    def get_house_system(self) -> str:
        """Get current house system setting."""
        return self.house_system