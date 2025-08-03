"""
Chart formatting utilities for converting raw astrology data to clean JSON format.
"""

from typing import Dict, List, Any
from datetime import datetime

def format_exact_degree(degree: float) -> str:
    """Format a decimal degree to degrees, minutes, seconds format."""
    deg = int(degree)
    min_val = int((degree % 1) * 60)
    sec = int(((degree % 1) * 60 % 1) * 60)
    return f"{deg}°{min_val:02d}'{sec:02d}\""

def create_simple_chart_response(raw_chart) -> Dict[str, Any]:
    """Create a simple, clean chart response from raw astrology data."""
    
    try:
        # Find key planets
        sun = next((p for p in raw_chart.planets if p.name == "Sun"), None)
        moon = next((p for p in raw_chart.planets if p.name == "Moon"), None)
        
        # Create placements array
        placements = []
        for planet in raw_chart.planets:
            placement = {
                "planet": planet.name,
                "sign": planet.sign,
                "house": planet.house,
                "degree": planet.degree,
                "exactDegree": format_exact_degree(planet.degree),
                "retrograde": getattr(planet, 'retro', False)
            }
            placements.append(placement)
        
        # Create simple response
        response = {
            "name": raw_chart.name,
            "birthDate": raw_chart.birth_info.date,
            "birthTime": raw_chart.birth_info.time,
            "location": raw_chart.birth_info.location,
            "coordinates": {
                "latitude": raw_chart.birth_info.latitude,
                "longitude": raw_chart.birth_info.longitude,
                "timezone": getattr(raw_chart.birth_info, 'timezone', None)
            },
            "houseSystem": "W",
            "risingSign": raw_chart.ascendant.sign,
            "sunSign": sun.sign if sun else "Unknown",
            "moonSign": moon.sign if moon else "Unknown",
            "ascendant": {
                "sign": raw_chart.ascendant.sign,
                "degree": raw_chart.ascendant.degree,
                "exactDegree": format_exact_degree(raw_chart.ascendant.degree)
            },
            "placements": placements,
            "generatedAt": datetime.now().isoformat()
        }
        
        return response
        
    except Exception as e:
        raise Exception(f"Chart formatting failed: {str(e)}")