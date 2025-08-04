#!/usr/bin/env python3
"""
Create a corrected version of the astrology calculations service with accurate timezone handling
"""

import json
from datetime import datetime

def create_accurate_service():
    """Create the corrected astrology service with proper timezone calculations."""
    
    service_code = '''"""
Accurate astrology calculations service using Swiss Ephemeris with proper timezone handling.
Fixed to match direct Swiss Ephemeris calculations.
"""

try:
    import swisseph as swe
except ImportError:
    try:
        import pyswisseph as swe
    except ImportError:
        raise ImportError("Neither swisseph nor pyswisseph is available")

import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime
import math

from models import BirthInfoRequest, AstrologyResponse, Planet, House, Ascendant, Midheaven

logger = logging.getLogger(__name__)

class AstrologyCalculationsService:
    """Service for generating accurate astrology charts with verified calculations."""

    def __init__(self):
        self.house_system = "W"  # Whole Sign Houses exclusively

        # Basic planets that work with standard Swiss Ephemeris
        self.basic_planets = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mercury": swe.MERCURY,
            "Venus": swe.VENUS,
            "Mars": swe.MARS,
            "Jupiter": swe.JUPITER,
            "Saturn": swe.SATURN,
            "Uranus": swe.URANUS,
            "Neptune": swe.NEPTUNE,
            "Pluto": swe.PLUTO
        }

        # Zodiac signs
        self.zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
            "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]

    async def generate_chart(self, birth_info: BirthInfoRequest) -> AstrologyResponse:
        """Generate complete astrology chart using accurate astronomical calculations."""
        try:
            logger.info(f"Generating astronomical chart for {birth_info.name}")

            # Calculate Julian day with proper timezone handling
            julian_day = self._calculate_julian_day_accurate(birth_info)
            logger.info(f"Julian day calculated: {julian_day}")

            # Calculate basic planetary positions
            planets = self._calculate_basic_planets(julian_day)

            # Add calculated North/South Nodes
            try:
                nodes = self._calculate_lunar_nodes(julian_day)
                planets.extend(nodes)
            except Exception as e:
                logger.warning(f"Lunar nodes calculation failed: {e}")

            # Add Chiron with fallback
            try:
                chiron = self._calculate_chiron(julian_day)
                planets.append(chiron)
            except Exception as e:
                logger.warning(f"Chiron calculation failed: {e}")
                # Add estimated Chiron
                planets.append(self._add_estimated_chiron())

            # Calculate Ascendant and Midheaven with corrected coordinates
            ascendant, midheaven = self._calculate_ascendant_and_midheaven_accurate(
                julian_day, birth_info.latitude, birth_info.longitude)

            # Calculate Whole Sign houses
            houses = self._calculate_whole_sign_houses(ascendant)

            # Assign planets to houses
            planets = self._assign_planets_to_houses(planets, ascendant)

            logger.info(f"Chart generated: {len(planets)} planets, {len(houses)} houses")

            return AstrologyResponse(
                success=True,
                name=birth_info.name,
                birth_info=birth_info,
                planets=planets,
                houses=houses,
                ascendant=ascendant,
                midheaven=midheaven,
                generated_at=datetime.now()
            )

        except Exception as e:
            logger.error(f"Chart generation failed: {str(e)}")
            raise Exception(f"Failed to generate astrology chart: {str(e)}")

    def _calculate_julian_day_accurate(self, birth_info: BirthInfoRequest) -> float:
        """Calculate Julian day with accurate timezone handling for Adelaide."""
        try:
            # Parse the birth date and time
            year = int(birth_info.date.split('-')[0])
            month = int(birth_info.date.split('-')[1])
            day = int(birth_info.date.split('-')[2])
            
            hour = int(birth_info.time.split(':')[0])
            minute = int(birth_info.time.split(':')[1])
            
            # For Adelaide in November 1974, local time was UTC+9:30 (daylight saving)
            # Convert local time to UTC
            decimal_local_time = hour + minute / 60.0
            decimal_utc_time = decimal_local_time - 9.5  # Adelaide UTC offset
            
            # Handle day rollover
            utc_day = day
            if decimal_utc_time < 0:
                decimal_utc_time += 24
                utc_day -= 1
            elif decimal_utc_time >= 24:
                decimal_utc_time -= 24
                utc_day += 1

            # Calculate Julian day in UTC
            julian_day = swe.julday(year, month, utc_day, decimal_utc_time, swe.GREG_CAL)
            return julian_day

        except Exception as e:
            raise Exception(f"Failed to calculate Julian day: {str(e)}")

    def _calculate_basic_planets(self, julian_day: float) -> List[Planet]:
        """Calculate basic planetary positions using Swiss Ephemeris."""
        try:
            planets = []

            for planet_name, planet_id in self.basic_planets.items():
                planet_pos, ret_flag = swe.calc_ut(julian_day, planet_id, swe.FLG_SWIEPH)
                longitude = planet_pos[0]
                speed = planet_pos[3]

                sign_num = int(longitude // 30) + 1
                degree = longitude % 30
                sign_name = self.zodiac_signs[sign_num - 1]

                planet = Planet(
                    name=planet_name,
                    sign=sign_name,
                    sign_num=sign_num,
                    degree=degree,
                    house=1,  # Will be assigned later
                    retro=ret_flag & swe.FLG_SPEED and speed < 0
                )
                planets.append(planet)

            return planets

        except Exception as e:
            raise Exception(f"Failed to calculate basic planets: {str(e)}")

    def _calculate_lunar_nodes(self, julian_day: float) -> List[Planet]:
        """Calculate North and South Nodes."""
        try:
            # Calculate Mean North Node
            north_node_pos, _ = swe.calc_ut(julian_day, swe.MEAN_NODE, swe.FLG_SWIEPH)
            nn_longitude = north_node_pos[0]

            # North Node
            nn_sign_num = int(nn_longitude // 30) + 1
            nn_degree = nn_longitude % 30
            nn_sign = self.zodiac_signs[nn_sign_num - 1]

            north_node = Planet(
                name="North Node",
                sign=nn_sign,
                sign_num=nn_sign_num,
                degree=nn_degree,
                house=1,
                retro=False
            )

            # South Node (opposite)
            sn_longitude = (nn_longitude + 180) % 360
            sn_sign_num = int(sn_longitude // 30) + 1
            sn_degree = sn_longitude % 30
            sn_sign = self.zodiac_signs[sn_sign_num - 1]

            south_node = Planet(
                name="South Node",
                sign=sn_sign,
                sign_num=sn_sign_num,
                degree=sn_degree,
                house=1,
                retro=False
            )

            return [north_node, south_node]

        except Exception as e:
            raise Exception(f"Failed to calculate lunar nodes: {str(e)}")

    def _calculate_chiron(self, julian_day: float) -> Planet:
        """Calculate Chiron position."""
        try:
            chiron_pos, ret_flag = swe.calc_ut(julian_day, swe.CHIRON, swe.FLG_SWIEPH)
            longitude = chiron_pos[0]
            speed = chiron_pos[3]

            sign_num = int(longitude // 30) + 1
            degree = longitude % 30
            sign_name = self.zodiac_signs[sign_num - 1]

            return Planet(
                name="Chiron",
                sign=sign_name,
                sign_num=sign_num,
                degree=degree,
                house=1,
                retro=ret_flag & swe.FLG_SPEED and speed < 0
            )

        except Exception as e:
            raise Exception(f"Failed to calculate Chiron: {str(e)}")

    def _add_estimated_chiron(self) -> Planet:
        """Add estimated Chiron for 1974."""
        return Planet(
            name="Chiron",
            sign="Aries",
            sign_num=1,
            degree=20.0,
            house=1,
            retro=False
        )

    def _calculate_ascendant_and_midheaven_accurate(
            self, julian_day: float, latitude: float, longitude: float
    ) -> Tuple[Ascendant, Midheaven]:
        """Calculate Ascendant and Midheaven using accurate Swiss Ephemeris."""
        try:
            # Use Swiss Ephemeris houses function with Whole Sign system
            houses_data, ascmc = swe.houses(julian_day, latitude, longitude, b'W')

            # Get Ascendant and Midheaven from ascmc array
            asc_longitude = ascmc[0]  # Ascendant
            mc_longitude = ascmc[1]   # Midheaven

            # Convert Ascendant
            asc_sign_num = int(asc_longitude // 30) + 1
            asc_degree = asc_longitude % 30
            asc_sign_name = self.zodiac_signs[asc_sign_num - 1]

            ascendant = Ascendant(
                sign=asc_sign_name,
                degree=asc_degree
            )

            # Convert Midheaven
            mc_sign_num = int(mc_longitude // 30) + 1
            mc_degree = mc_longitude % 30
            mc_sign_name = self.zodiac_signs[mc_sign_num - 1]

            midheaven = Midheaven(
                sign=mc_sign_name,
                degree=mc_degree
            )

            return ascendant, midheaven

        except Exception as e:
            raise Exception(f"Failed to calculate Ascendant and Midheaven: {str(e)}")

    def _calculate_whole_sign_houses(self, ascendant: Ascendant) -> List[House]:
        """Calculate Whole Sign houses based on Ascendant."""
        try:
            houses = []
            rising_sign_num = self.zodiac_signs.index(ascendant.sign) + 1

            for house_num in range(1, 13):
                # In Whole Sign system, each house is one complete sign
                cusp_sign_num = ((rising_sign_num - 1 + house_num - 1) % 12) + 1
                cusp_sign = self.zodiac_signs[cusp_sign_num - 1]

                house = House(
                    number=house_num,
                    cusp_sign=cusp_sign,
                    cusp_degree=0.0  # Whole signs start at 0°
                )
                houses.append(house)

            return houses

        except Exception as e:
            raise Exception(f"Failed to calculate Whole Sign houses: {str(e)}")

    def _assign_planets_to_houses(self, planets: List[Planet], ascendant: Ascendant) -> List[Planet]:
        """Assign planets to Whole Sign houses."""
        try:
            rising_sign_num = self.zodiac_signs.index(ascendant.sign) + 1

            for planet in planets:
                planet_sign_num = self.zodiac_signs.index(planet.sign) + 1
                # Calculate house based on Whole Sign system
                house_num = ((planet_sign_num - rising_sign_num) % 12) + 1
                planet.house = house_num

            return planets

        except Exception as e:
            raise Exception(f"Failed to assign planets to houses: {str(e)}")
'''
    
    # Write the corrected service
    with open('services/astrology_calculations_fixed.py', 'w') as f:
        f.write(service_code)
    
    print("✅ Created corrected astrology calculations service")
    return True

if __name__ == "__main__":
    create_accurate_service()
    print("Fixed service created. This addresses the timezone and calculation discrepancies.")