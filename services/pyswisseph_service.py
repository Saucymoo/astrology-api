"""
PySwissEph service for accurate astronomical calculations.
Uses Swiss Ephemeris data for precise planetary positions and house calculations.
"""

import swisseph as swe
import logging
from typing import Dict, List, Any
from datetime import datetime
import math

from models import BirthInfoRequest, AstrologyResponse, Planet, House, Ascendant

logger = logging.getLogger(__name__)


class PySwissEphService:
    """Service for generating astrology charts using PySwissEph (Swiss Ephemeris)."""
    
    def __init__(self):
        self.house_system = "W"  # Whole Sign Houses
        
        # Planet mapping to Swiss Ephemeris constants
        self.planets = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mercury": swe.MERCURY,
            "Venus": swe.VENUS,
            "Mars": swe.MARS,
            "Jupiter": swe.JUPITER,
            "Saturn": swe.SATURN,
            "Uranus": swe.URANUS,
            "Neptune": swe.NEPTUNE,
            "Pluto": swe.PLUTO,
            "Chiron": swe.CHIRON,
            "North Node": swe.TRUE_NODE,
            "South Node": swe.TRUE_NODE  # Will calculate opposite
        }
        
        # Zodiac signs
        self.zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
    
    async def generate_chart(self, birth_info: BirthInfoRequest) -> AstrologyResponse:
        """Generate complete astrology chart using Swiss Ephemeris."""
        try:
            logger.info(f"Generating Swiss Ephemeris chart for {birth_info.name}")
            
            # Calculate Julian day from birth information
            julian_day = self._calculate_julian_day(birth_info)
            logger.info(f"Julian day: {julian_day}")
            
            # Calculate ascendant using house calculation
            ascendant = self._calculate_ascendant(julian_day, birth_info.latitude, birth_info.longitude)
            logger.info(f"Ascendant: {ascendant.sign} {ascendant.degree:.6f}°")
            
            # Calculate planetary positions
            planets = self._calculate_planetary_positions(julian_day)
            logger.info(f"Calculated {len(planets)} planetary positions")
            
            # Calculate houses using Whole Sign system
            houses = self._calculate_whole_sign_houses(ascendant)
            
            # Assign planets to houses using Whole Sign logic
            planets = self._assign_planets_to_houses(planets, ascendant)
            
            return AstrologyResponse(
                success=True,
                name=birth_info.name,
                birth_info=birth_info,
                planets=planets,
                houses=houses,
                ascendant=ascendant,
                generated_at=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Swiss Ephemeris chart generation failed: {str(e)}")
            raise Exception(f"Failed to generate astrology chart: {str(e)}")
    
    def _calculate_julian_day(self, birth_info: BirthInfoRequest) -> float:
        """Calculate Julian day from birth information."""
        try:
            # Parse date (YYYY-MM-DD format from validated birth_info)
            date_parts = birth_info.date.split('-')
            year = int(date_parts[0])
            month = int(date_parts[1])
            day = int(date_parts[2])
            
            # Parse time
            time_parts = birth_info.time.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            
            # Convert to decimal hours
            decimal_hour = hour + minute / 60.0
            
            # Adjust for timezone (convert to UTC)
            if hasattr(birth_info, 'timezone') and birth_info.timezone:
                decimal_hour -= birth_info.timezone
                
                # Handle day rollover if needed
                if decimal_hour < 0:
                    decimal_hour += 24
                    day -= 1
                elif decimal_hour >= 24:
                    decimal_hour -= 24
                    day += 1
            
            # Calculate Julian day using Swiss Ephemeris
            julian_day = swe.julday(year, month, day, decimal_hour, swe.GREG_CAL)
            
            return julian_day
            
        except Exception as e:
            raise Exception(f"Failed to calculate Julian day: {str(e)}")
    
    def _calculate_ascendant(self, julian_day: float, latitude: float, longitude: float) -> Ascendant:
        """Calculate the Ascendant using Swiss Ephemeris house calculation."""
        try:
            # Calculate houses using Placidus to get accurate Ascendant
            # Then we'll use this Ascendant for Whole Sign house calculation
            houses_data, ascmc = swe.houses(julian_day, latitude, longitude, b'P')
            
            # Ascendant is the first element in ascmc array
            asc_longitude = ascmc[0]
            
            # Convert longitude to sign and degree
            sign_num = int(asc_longitude // 30) + 1
            degree = asc_longitude % 30
            sign_name = self.zodiac_signs[sign_num - 1]
            
            return Ascendant(
                sign=sign_name,
                degree=degree
            )
            
        except Exception as e:
            raise Exception(f"Failed to calculate Ascendant: {str(e)}")
    
    def _calculate_planetary_positions(self, julian_day: float) -> List[Planet]:
        """Calculate positions for all planets using Swiss Ephemeris."""
        try:
            calculated_planets = []
            
            for planet_name, planet_id in self.planets.items():
                if planet_name == "South Node":
                    # Calculate South Node as opposite of North Node
                    north_node_pos, _ = swe.calc_ut(julian_day, swe.TRUE_NODE, swe.FLG_SWIEPH)
                    longitude = (north_node_pos[0] + 180) % 360
                    speed = -north_node_pos[3]  # Opposite speed direction
                else:
                    # Calculate planet position
                    planet_pos, _ = swe.calc_ut(julian_day, planet_id, swe.FLG_SWIEPH)
                    longitude = planet_pos[0]
                    speed = planet_pos[3]
                
                # Convert longitude to sign and degree
                sign_num = int(longitude // 30) + 1
                degree = longitude % 30
                sign_name = self.zodiac_signs[sign_num - 1]
                
                # Determine if retrograde (negative speed for most planets)
                # Note: Sun and Moon are never retrograde
                is_retrograde = False
                if planet_name not in ["Sun", "Moon"]:
                    is_retrograde = speed < 0
                
                planet = Planet(
                    name=planet_name,
                    sign=sign_name,
                    sign_num=sign_num,
                    degree=degree,
                    house=1,  # Will be assigned later using Whole Sign logic
                    retro=is_retrograde
                )
                
                calculated_planets.append(planet)
                
                logger.debug(f"{planet_name}: {sign_name} {degree:.6f}° (Retrograde: {is_retrograde})")
            
            return calculated_planets
            
        except Exception as e:
            raise Exception(f"Failed to calculate planetary positions: {str(e)}")
    
    def _calculate_whole_sign_houses(self, ascendant: Ascendant) -> List[House]:
        """Calculate house cusps using Whole Sign system."""
        try:
            houses = []
            
            # Find rising sign index in zodiac
            rising_sign_index = self.zodiac_signs.index(ascendant.sign)
            
            # In Whole Sign system:
            # - House 1 = Rising sign
            # - House 2 = Next sign
            # - Each house cusp is at 0° of its sign
            for house_num in range(1, 13):
                house_sign_index = (rising_sign_index + house_num - 1) % 12
                house_sign = self.zodiac_signs[house_sign_index]
                
                house = House(
                    house=house_num,
                    sign=house_sign,
                    sign_num=house_sign_index + 1,
                    degree=0.0  # Whole Sign houses always start at 0°
                )
                
                houses.append(house)
            
            return houses
            
        except Exception as e:
            raise Exception(f"Failed to calculate houses: {str(e)}")
    
    def _assign_planets_to_houses(self, planets: List[Planet], ascendant: Ascendant) -> List[Planet]:
        """Assign planets to houses using Whole Sign logic."""
        try:
            rising_sign_index = self.zodiac_signs.index(ascendant.sign)
            
            for planet in planets:
                planet_sign_index = self.zodiac_signs.index(planet.sign)
                
                # In Whole Sign system, house number is determined solely by sign
                # Calculate which house this planet's sign falls into
                house_num = ((planet_sign_index - rising_sign_index) % 12) + 1
                planet.house = house_num
                
                logger.debug(f"{planet.name} in {planet.sign} → House {house_num}")
            
            return planets
            
        except Exception as e:
            raise Exception(f"Failed to assign planets to houses: {str(e)}")
    
    def set_house_system(self, house_system: str) -> None:
        """Set house system."""
        if house_system != "W":
            logger.warning(f"Only Whole Sign (W) houses fully supported, setting to W")
        self.house_system = "W"
    
    def get_house_system(self) -> str:
        """Get current house system."""
        return self.house_system