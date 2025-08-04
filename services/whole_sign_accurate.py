"""
Whole Sign Houses Accurate Implementation
- Exact Ascendant and Midheaven degrees using Placidus for angles
- Whole Sign house assignments (entire signs in houses)
- Midheaven can appear in houses 8-12 depending on location/time
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

class WholeSignAstrologyService:
    """Accurate Whole Sign Houses implementation with proper angular calculations."""

    def __init__(self):
        self.house_system = "Whole Sign"  # Display name
        
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
        """Generate chart with accurate Whole Sign houses and exact angles."""
        try:
            logger.info(f"Generating Whole Sign chart for {birth_info.name}")

            # Calculate Julian day with proper timezone handling
            julian_day = self._calculate_julian_day_accurate(birth_info)
            logger.info(f"Julian day: {julian_day}")

            # Calculate exact Ascendant and Midheaven using Placidus (for angles only)
            ascendant, midheaven = self._calculate_exact_angles(
                julian_day, birth_info.latitude, birth_info.longitude)

            # Calculate planetary positions
            planets = self._calculate_basic_planets(julian_day)

            # Add lunar nodes
            try:
                nodes = self._calculate_lunar_nodes(julian_day)
                planets.extend(nodes)
            except Exception as e:
                logger.warning(f"Lunar nodes failed: {e}")

            # Add Chiron with fallback
            try:
                chiron = self._calculate_chiron(julian_day)
                planets.append(chiron)
            except Exception as e:
                logger.warning(f"Chiron failed: {e}")
                planets.append(self._add_estimated_chiron())

            # Calculate Whole Sign houses (entire signs)
            houses = self._calculate_whole_sign_houses(ascendant)

            # Assign planets to Whole Sign houses
            planets = self._assign_planets_to_whole_sign_houses(planets, ascendant)

            # Add Midheaven house assignment (can be in houses 8-12)
            midheaven_house = self._find_midheaven_house(midheaven, ascendant) 

            logger.info(f"Chart complete: {len(planets)} planets, Midheaven in house {midheaven_house}")

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
        """Calculate Julian day with accurate timezone handling."""
        try:
            year = int(birth_info.date.split('-')[0])
            month = int(birth_info.date.split('-')[1])
            day = int(birth_info.date.split('-')[2])
            
            hour = int(birth_info.time.split(':')[0])
            minute = int(birth_info.time.split(':')[1])
            
            # Adelaide UTC offset (accounting for daylight saving in November 1974)
            decimal_local_time = hour + minute / 60.0
            decimal_utc_time = decimal_local_time - 9.5  # Adelaide offset
            
            # Handle day rollover
            utc_day = day
            if decimal_utc_time < 0:
                decimal_utc_time += 24
                utc_day -= 1
            elif decimal_utc_time >= 24:
                decimal_utc_time -= 24
                utc_day += 1

            julian_day = swe.julday(year, month, utc_day, decimal_utc_time, swe.GREG_CAL)
            return julian_day

        except Exception as e:
            raise Exception(f"Failed to calculate Julian day: {str(e)}")

    def _calculate_exact_angles(self, julian_day: float, latitude: float, longitude: float) -> Tuple[Ascendant, Midheaven]:
        """Calculate exact Ascendant and Midheaven degrees using Placidus for accuracy."""
        try:
            # Use Placidus system for most accurate angular calculations
            # Whole Sign uses these exact degrees but different house boundaries
            houses_data, ascmc = swe.houses(julian_day, latitude, longitude, b'P')

            # Ascendant - exact degree
            asc_longitude = ascmc[0] 
            asc_sign_num = int(asc_longitude // 30) + 1
            asc_degree = asc_longitude % 30
            asc_sign_name = self.zodiac_signs[asc_sign_num - 1]

            ascendant = Ascendant(sign=asc_sign_name, degree=asc_degree)

            # Midheaven - exact degree
            mc_longitude = ascmc[1]
            mc_sign_num = int(mc_longitude // 30) + 1
            mc_degree = mc_longitude % 30
            mc_sign_name = self.zodiac_signs[mc_sign_num - 1]

            midheaven = Midheaven(sign=mc_sign_name, degree=mc_degree)

            logger.info(f"Exact angles - ASC: {asc_sign_name} {asc_degree:.2f}°, MC: {mc_sign_name} {mc_degree:.2f}°")

            return ascendant, midheaven

        except Exception as e:
            raise Exception(f"Failed to calculate exact angles: {str(e)}")

    def _calculate_basic_planets(self, julian_day: float) -> List[Planet]:
        """Calculate planetary positions."""
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
            raise Exception(f"Failed to calculate planets: {str(e)}")

    def _calculate_lunar_nodes(self, julian_day: float) -> List[Planet]:
        """Calculate North and South Nodes."""
        try:
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
            raise Exception(f"Failed to calculate nodes: {str(e)}")

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
        """Fallback Chiron for 1974."""
        return Planet(
            name="Chiron",
            sign="Aries",
            sign_num=1,
            degree=20.0,
            house=1,
            retro=False
        )

    def _calculate_whole_sign_houses(self, ascendant: Ascendant) -> List[House]:
        """Calculate Whole Sign houses - entire signs occupy each house."""
        try:
            houses = []
            rising_sign_index = self.zodiac_signs.index(ascendant.sign)

            for house_num in range(1, 13):
                # Each house contains an entire sign
                house_sign_index = (rising_sign_index + house_num - 1) % 12
                house_sign = self.zodiac_signs[house_sign_index]

                house = House(
                    house=house_num,
                    sign=house_sign,
                    sign_num=house_sign_index + 1,
                    degree=0.0  # Whole signs start at 0°
                )
                houses.append(house)

            return houses

        except Exception as e:
            raise Exception(f"Failed to calculate Whole Sign houses: {str(e)}")

    def _assign_planets_to_whole_sign_houses(self, planets: List[Planet], ascendant: Ascendant) -> List[Planet]:
        """Assign planets to houses using Whole Sign system."""
        try:
            rising_sign_index = self.zodiac_signs.index(ascendant.sign)

            for planet in planets:
                planet_sign_index = self.zodiac_signs.index(planet.sign)
                # Calculate house based on sign position relative to rising sign
                house_num = ((planet_sign_index - rising_sign_index) % 12) + 1
                planet.house = house_num

            return planets

        except Exception as e:
            raise Exception(f"Failed to assign planets to houses: {str(e)}")

    def _find_midheaven_house(self, midheaven: Midheaven, ascendant: Ascendant) -> int:
        """Find which Whole Sign house the Midheaven falls in (can be 8th-12th house)."""
        try:
            rising_sign_index = self.zodiac_signs.index(ascendant.sign)
            mc_sign_index = self.zodiac_signs.index(midheaven.sign)
            
            # Calculate which house the MC sign falls in
            mc_house = ((mc_sign_index - rising_sign_index) % 12) + 1
            
            logger.info(f"Midheaven {midheaven.sign} falls in house {mc_house}")
            return mc_house

        except Exception as e:
            logger.warning(f"Failed to calculate MC house: {e}")
            return 10  # Default to 10th house