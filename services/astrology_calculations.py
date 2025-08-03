"""
Astrological calculation utilities for enhanced chart data.
Includes functions for chart rulers, moon phases, house rulers, and degree formatting.
"""

import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from models_chart_points import ChartRuler, MoonPhase, HouseInfo, Ascendant


class AstrologyCalculations:
    """Utility class for astrological calculations."""
    
    def __init__(self):
        # Traditional planetary rulers for each sign
        self.sign_rulers = {
            "Aries": "Mars",
            "Taurus": "Venus", 
            "Gemini": "Mercury",
            "Cancer": "Moon",
            "Leo": "Sun",
            "Virgo": "Mercury",
            "Libra": "Venus",
            "Scorpio": "Mars",  # Traditional ruler
            "Sagittarius": "Jupiter",
            "Capricorn": "Saturn",
            "Aquarius": "Saturn",  # Traditional ruler
            "Pisces": "Jupiter"  # Traditional ruler
        }
        
        # Modern rulers (for reference, but using traditional for chart ruler)
        self.modern_rulers = {
            "Scorpio": "Pluto",
            "Aquarius": "Uranus", 
            "Pisces": "Neptune"
        }
        
        # Zodiac signs in order
        self.zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
    
    def format_exact_degree(self, degree: float) -> str:
        """Convert decimal degree to exact degree format (XX°XX'XX")."""
        degrees = int(degree)
        minutes_float = (degree - degrees) * 60
        minutes = int(minutes_float)
        seconds = int((minutes_float - minutes) * 60)
        
        return f"{degrees}°{minutes:02d}'{seconds:02d}\""
    
    def get_chart_ruler(self, ascendant_sign: str, planets: List) -> ChartRuler:
        """Determine the chart ruler based on the rising sign."""
        ruler_planet_name = self.sign_rulers.get(ascendant_sign, "Sun")
        
        # Find the ruling planet in the chart
        ruling_planet = next((p for p in planets if p.name == ruler_planet_name), None)
        
        if ruling_planet:
            return ChartRuler(
                planet=ruling_planet.name,
                sign=ruling_planet.sign,
                house=ruling_planet.house,
                degree=ruling_planet.degree,
                exactDegree=self.format_exact_degree(ruling_planet.degree),
                retrograde=getattr(ruling_planet, 'retro', False)
            )
        else:
            # Fallback if ruler not found
            return ChartRuler(
                planet=ruler_planet_name,
                sign="Unknown",
                house=1,
                degree=0.0,
                exactDegree="0°00'00\"",
                retrograde=False
            )
    
    def calculate_moon_phase(self, birth_date: str, sun_degree: float, moon_degree: float) -> MoonPhase:
        """Calculate moon phase information based on Sun-Moon angular relationship."""
        # Calculate the angular distance between Sun and Moon
        angular_distance = (moon_degree - sun_degree) % 360
        
        # Determine moon phase based on angular distance
        if angular_distance < 45 or angular_distance >= 315:
            phase_name = "New Moon"
            illumination = 0.0
        elif 45 <= angular_distance < 90:
            phase_name = "Waxing Crescent"
            illumination = 25.0
        elif 90 <= angular_distance < 135:
            phase_name = "First Quarter"
            illumination = 50.0
        elif 135 <= angular_distance < 180:
            phase_name = "Waxing Gibbous"
            illumination = 75.0
        elif 180 <= angular_distance < 225:
            phase_name = "Full Moon"
            illumination = 100.0
        elif 225 <= angular_distance < 270:
            phase_name = "Waning Gibbous"
            illumination = 75.0
        else:  # 270 <= angular_distance < 315
            phase_name = "Last Quarter"
            illumination = 50.0
        
        # Note: Void of course calculation would require ephemeris data
        # For now, we'll use a simplified approximation
        is_void = self._estimate_void_of_course(moon_degree)
        
        return MoonPhase(
            phaseName=phase_name,
            illumination=illumination,
            isVoidOfCourse=is_void,
            nextAspect=self._get_next_moon_aspect(moon_degree)
        )
    
    def _estimate_void_of_course(self, moon_degree: float) -> bool:
        """Simplified void of course estimation (would need real ephemeris data for accuracy)."""
        # This is a simplified approximation - real VOC requires ephemeris data
        # Return false for now, as accurate VOC requires planetary position predictions
        return False
    
    def _get_next_moon_aspect(self, moon_degree: float) -> Optional[str]:
        """Estimate next major Moon aspect (simplified)."""
        # This would need real ephemeris data for accuracy
        # Return None for now as accurate aspect calculation requires planetary motion data
        return None
    
    def generate_house_breakdown(self, ascendant_sign: str, planets: List) -> List[HouseInfo]:
        """Generate complete house breakdown for Whole Sign system."""
        houses = []
        
        # Get starting sign index for 1st house
        ascendant_index = self.zodiac_signs.index(ascendant_sign)
        
        for house_num in range(1, 13):
            # In Whole Sign, each house = one complete sign
            house_sign_index = (ascendant_index + house_num - 1) % 12
            house_sign = self.zodiac_signs[house_sign_index]
            
            # Get traditional ruler of this house sign
            house_ruler = self.sign_rulers.get(house_sign, "Unknown")
            
            # Find planets in this house
            planets_in_house = [p.name for p in planets if p.house == house_num]
            
            house_info = HouseInfo(
                house=house_num,
                sign=house_sign,
                ruler=house_ruler,
                planets=planets_in_house
            )
            houses.append(house_info)
        
        return houses
    
    def create_enhanced_ascendant(self, ascendant) -> Ascendant:
        """Create enhanced ascendant information with exact degree."""
        return Ascendant(
            sign=ascendant.sign,
            degree=ascendant.degree,
            exactDegree=self.format_exact_degree(ascendant.degree)
        )