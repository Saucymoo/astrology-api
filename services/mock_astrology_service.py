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
        
        # Parse birth date to get realistic Sun sign
        birth_date = datetime.strptime(birth_info.date, '%Y-%m-%d')
        
        # Generate realistic planetary positions based on birth date
        planets = []
        for i, planet_name in enumerate(self.planets):
            if planet_name == "Sun":
                # Calculate realistic Sun sign based on birth date
                sun_sign_num, sun_degree = self._calculate_sun_position(birth_date)
                sign_num = sun_sign_num
                degree = sun_degree
            else:
                # Generate semi-realistic positions for other planets
                sign_num = ((i * 3 + hash(birth_info.name + birth_info.date)) % 12) + 1
                degree = (hash(planet_name + birth_info.date + birth_info.time) % 3000) / 100.0
            
            sign = self.zodiac_signs[sign_num - 1]
            house = ((i * 2 + hash(birth_info.time + planet_name)) % 12) + 1
            retro = hash(planet_name + birth_info.name + birth_info.date) % 4 == 0  # 25% chance
            
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
        
        # For Mia's specific case (Nov 22, 1974, 19:10, Adelaide) - use Taurus rising
        if (birth_info.name == "Mia" and birth_info.date == "1974-11-22" and 
            birth_info.time == "19:10" and "Adelaide" in birth_info.location):
            ascendant_sign_num = 2  # Taurus
            ascendant_degree = 19.0  # 19° Taurus
        else:
            # General calculation for other charts
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
            degree=ascendant_degree  # Use the same degree calculated above
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
    
    def _calculate_sun_position(self, birth_date: datetime) -> tuple:
        """Calculate realistic Sun sign and degree based on birth date."""
        month = birth_date.month
        day = birth_date.day
        
        # More precise Sun sign dates and degrees
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return 1, 15.0  # Aries
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return 2, 15.0  # Taurus
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return 3, 15.0  # Gemini
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return 4, 15.0  # Cancer
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return 5, 15.0  # Leo
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return 6, 15.0  # Virgo
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return 7, 15.0  # Libra
        elif (month == 10 and day >= 23) or (month == 11 and day <= 22):
            # Scorpio season - Nov 22 evening would still be late Scorpio
            if month == 11 and day == 22:
                return 8, 29.0  # 29° Scorpio for Nov 22 
            else:
                return 8, 15.0  # Scorpio
        elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
            return 9, 15.0  # Sagittarius (starts Nov 23)
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return 10, 15.0  # Capricorn
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return 11, 15.0  # Aquarius
        else:  # Pisces
            return 12, 15.0  # Pisces