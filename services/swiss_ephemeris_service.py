"""
Swiss Ephemeris service for accurate astronomical calculations.
This service uses the Swiss Ephemeris library for precise planetary positions.
"""

import swisseph as swe
import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime, timezone, timedelta
import math

from models import BirthInfoRequest, AstrologyResponse, Planet, House, Ascendant

logger = logging.getLogger(__name__)


class SwissEphemerisService:
    """Service for generating astrology charts using Swiss Ephemeris."""
    
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
        """
        Generate a complete astrology chart using Swiss Ephemeris.
        
        Args:
            birth_info: Birth details including date, time, and location
            
        Returns:
            AstrologyResponse: Complete chart with planets, houses, and ascendant
        """
        try:
            logger.info(f"Generating Swiss Ephemeris chart for {birth_info.name}")
            
            # Parse birth date and time
            birth_datetime = self._parse_birth_datetime(birth_info)
            julian_day = self._calculate_julian_day(birth_datetime)
            
            logger.info(f"Birth datetime: {birth_datetime}")
            logger.info(f"Julian day: {julian_day}")
            
            # Calculate planetary positions
            planets = self._calculate_planetary_positions(julian_day)
            
            # Calculate ascendant (rising sign)
            ascendant = self._calculate_ascendant(
                julian_day, 
                birth_info.latitude, 
                birth_info.longitude
            )
            
            # Calculate houses using Whole Sign system
            houses = self._calculate_whole_sign_houses(ascendant)
            
            # Assign planets to houses using Whole Sign logic
            planets = self._assign_planets_to_houses(planets, ascendant)
            
            logger.info(f"Generated chart with {len(planets)} planets, {len(houses)} houses")
            
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
    
    def _parse_birth_datetime(self, birth_info: BirthInfoRequest) -> datetime:
        """Parse birth date and time into datetime object."""
        try:
            # Parse date (YYYY-MM-DD format)
            date_parts = birth_info.date.split('-')
            year = int(date_parts[0])
            month = int(date_parts[1])
            day = int(date_parts[2])
            
            # Parse time
            time_parts = birth_info.time.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            
            # Create datetime in local timezone
            birth_dt = datetime(year, month, day, hour, minute)
            
            # Convert to UTC if timezone info is available
            if hasattr(birth_info, 'timezone') and birth_info.timezone:
                # Create timezone offset
                tz_offset = timedelta(hours=birth_info.timezone)
                utc_dt = birth_dt - tz_offset
                return utc_dt
            
            return birth_dt
            
        except Exception as e:
            raise Exception(f"Failed to parse birth datetime: {str(e)}")
    
    def _calculate_julian_day(self, birth_datetime: datetime) -> float:
        """Calculate Julian day number for the birth datetime."""
        try:
            year = birth_datetime.year
            month = birth_datetime.month
            day = birth_datetime.day
            hour = birth_datetime.hour + birth_datetime.minute / 60.0
            
            # Swiss Ephemeris Julian day calculation
            julian_day = swe.julday(year, month, day, hour, swe.GREG_CAL)
            
            return julian_day
            
        except Exception as e:
            raise Exception(f"Failed to calculate Julian day: {str(e)}")
    
    def _calculate_planetary_positions(self, julian_day: float) -> List[Planet]:
        """Calculate positions for all planets."""
        try:
            calculated_planets = []
            
            for planet_name, planet_id in self.planets.items():
                if planet_name == "South Node":
                    # Calculate South Node as opposite of North Node
                    north_node_pos, _ = swe.calc_ut(julian_day, swe.TRUE_NODE, swe.FLG_SWIEPH)
                    longitude = (north_node_pos[0] + 180) % 360  # Opposite position
                    speed = -north_node_pos[3]  # Opposite speed
                else:
                    # Calculate planet position
                    planet_pos, _ = swe.calc_ut(julian_day, planet_id, swe.FLG_SWIEPH)
                    longitude = planet_pos[0]
                    speed = planet_pos[3]
                
                # Convert longitude to sign and degree
                sign_num = int(longitude // 30) + 1
                degree = longitude % 30
                sign_name = self.zodiac_signs[sign_num - 1]
                
                # Check if retrograde (negative speed)
                is_retrograde = speed < 0
                
                planet = Planet(
                    name=planet_name,
                    sign=sign_name,
                    sign_num=sign_num,
                    degree=degree,
                    house=1,  # Will be assigned later
                    retro=is_retrograde
                )
                
                calculated_planets.append(planet)
                
                logger.info(f"{planet_name}: {sign_name} {degree:.6f}° (Retrograde: {is_retrograde})")
            
            return calculated_planets
            
        except Exception as e:
            raise Exception(f"Failed to calculate planetary positions: {str(e)}")
    
    def _calculate_ascendant(self, julian_day: float, latitude: float, longitude: float) -> Ascendant:
        """Calculate the Ascendant (Rising Sign)."""
        try:
            # Calculate houses using Placidus first to get accurate Ascendant
            houses_data, ascmc = swe.houses(julian_day, latitude, longitude, b'P')
            
            # Ascendant is the first value in ascmc array
            asc_longitude = ascmc[0]
            
            # Convert to sign and degree
            sign_num = int(asc_longitude // 30) + 1
            degree = asc_longitude % 30
            sign_name = self.zodiac_signs[sign_num - 1]
            
            logger.info(f"Ascendant: {sign_name} {degree:.6f}°")
            
            return Ascendant(
                sign=sign_name,
                degree=degree
            )
            
        except Exception as e:
            raise Exception(f"Failed to calculate Ascendant: {str(e)}")
    
    def _calculate_whole_sign_houses(self, ascendant: Ascendant) -> List[House]:
        """Calculate house cusps using Whole Sign system."""
        try:
            houses = []
            
            # Find rising sign index
            rising_sign_index = self.zodiac_signs.index(ascendant.sign)
            
            # In Whole Sign system, each house starts at 0° of its sign
            for house_num in range(1, 13):
                house_sign_index = (rising_sign_index + house_num - 1) % 12
                house_sign = self.zodiac_signs[house_sign_index]
                
                house = House(
                    house=house_num,
                    sign=house_sign,
                    sign_num=house_sign_index + 1,
                    degree=0.0  # Whole Sign houses start at 0°
                )
                
                houses.append(house)
            
            logger.info("Calculated Whole Sign houses")
            return houses
            
        except Exception as e:
            raise Exception(f"Failed to calculate houses: {str(e)}")
    
    def _assign_planets_to_houses(self, planets: List[Planet], ascendant: Ascendant) -> List[Planet]:
        """Assign planets to houses using Whole Sign logic."""
        try:
            rising_sign_index = self.zodiac_signs.index(ascendant.sign)
            
            for planet in planets:
                planet_sign_index = self.zodiac_signs.index(planet.sign)
                
                # Calculate house number using Whole Sign logic
                # House = (planet_sign_index - rising_sign_index) + 1, wrapped around
                house_num = ((planet_sign_index - rising_sign_index) % 12) + 1
                planet.house = house_num
                
                logger.info(f"{planet.name} in {planet.sign} → House {house_num}")
            
            return planets
            
        except Exception as e:
            raise Exception(f"Failed to assign planets to houses: {str(e)}")
    
    def set_house_system(self, house_system: str) -> None:
        """Set house system (only Whole Sign supported)."""
        if house_system != "W":
            logger.warning(f"Only Whole Sign (W) houses supported, ignoring {house_system}")
        self.house_system = "W"
    
    def get_house_system(self) -> str:
        """Get current house system."""
        return self.house_system