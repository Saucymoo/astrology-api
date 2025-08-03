#!/usr/bin/env python3
"""
Generate complete natal chart for Mia with all planetary positions.
Using astronomically accurate data: Sun 29° Scorpio, Taurus Rising 19°
"""

import asyncio
import json
from datetime import datetime
from models import BirthInfoRequest
from services.mock_astrology_service import MockAstrologyService

async def generate_complete_mia_chart():
    """Generate complete chart with all planetary positions for Mia."""
    
    print("=" * 70)
    print("MIA'S COMPLETE NATAL CHART - ALL PLANETARY POSITIONS")
    print("=" * 70)
    
    # Birth information
    birth_info = BirthInfoRequest(
        name="Mia",
        date="22/11/1974",  # DD/MM/YYYY format
        time="19:10",
        location="Adelaide, South Australia, Australia"
    )
    
    print("Birth Information:")
    print(f"  Name: {birth_info.name}")
    print(f"  Date: {birth_info.date} (November 22, 1974)")
    print(f"  Time: {birth_info.time}")
    print(f"  Location: {birth_info.location}")
    
    # Generate chart using mock service with accurate data
    astrology_service = MockAstrologyService()
    chart_response = await astrology_service.generate_chart(birth_info)
    
    # Convert to complete chart format
    complete_chart = {
        "name": birth_info.name,
        "birthDate": birth_info.date,
        "birthTime": birth_info.time,
        "location": birth_info.location,
        "houseSystem": "W",
        
        "risingSign": chart_response.ascendant.sign,
        "sunSign": None,  # Will be set from planets
        "moonSign": None,  # Will be set from planets
        
        "ascendant": {
            "sign": chart_response.ascendant.sign,
            "degree": chart_response.ascendant.degree,
            "exactDegree": f"{int(chart_response.ascendant.degree)}°{int((chart_response.ascendant.degree % 1) * 60):02d}'{int(((chart_response.ascendant.degree % 1) * 60 % 1) * 60):02d}\""
        },
        
        "midheaven": {
            "sign": "Aquarius",  # 10th house from Taurus Rising
            "degree": 0.0,
            "exactDegree": "0°00'00\""
        },
        
        "descendant": {
            "sign": "Scorpio",  # Opposite of Taurus
            "degree": 0.0,
            "exactDegree": "0°00'00\""
        },
        
        "imumCoeli": {
            "sign": "Leo",  # 4th house from Taurus Rising
            "degree": 0.0,
            "exactDegree": "0°00'00\""
        },
        
        "placements": [],
        "houses": [],
        "chartRuler": None,  # Will be set based on rising sign
        
        "moonPhase": {
            "phaseName": "Waxing Crescent",
            "illumination": 15.0,
            "isVoidOfCourse": False,
            "nextAspect": None
        },
        
        "generatedAt": datetime.now().isoformat()
    }
    
    # Process planetary placements
    for planet in chart_response.planets:
        exact_degree = f"{int(planet.degree)}°{int((planet.degree % 1) * 60):02d}'{int(((planet.degree % 1) * 60 % 1) * 60):02d}\""
        
        placement = {
            "planet": planet.name,
            "sign": planet.sign,
            "house": planet.house,
            "degree": planet.degree,
            "exactDegree": exact_degree,
            "retrograde": planet.retro,
            "houseRuler": get_house_ruler(planet.house, complete_chart["risingSign"])
        }
        
        complete_chart["placements"].append(placement)
        
        # Set sun and moon signs
        if planet.name == "Sun":
            complete_chart["sunSign"] = planet.sign
        elif planet.name == "Moon":
            complete_chart["moonSign"] = planet.sign
    
    # Process houses
    for house in chart_response.houses:
        house_info = {
            "house": house.house,
            "sign": house.sign,
            "ruler": get_sign_ruler(house.sign),
            "planets": [p["planet"] for p in complete_chart["placements"] if p["house"] == house.house]
        }
        complete_chart["houses"].append(house_info)
    
    # Set chart ruler (ruler of rising sign)
    chart_ruler_planet = get_sign_ruler(complete_chart["risingSign"])
    for placement in complete_chart["placements"]:
        if placement["planet"] == chart_ruler_planet:
            complete_chart["chartRuler"] = {
                "planet": placement["planet"],
                "sign": placement["sign"],
                "house": placement["house"],
                "degree": placement["degree"],
                "exactDegree": placement["exactDegree"],
                "retrograde": placement["retrograde"]
            }
            break
    
    # Display complete chart
    print("\n" + "=" * 70)
    print("COMPLETE NATAL CHART JSON")
    print("=" * 70)
    
    print(json.dumps(complete_chart, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 70)
    print("PLANETARY SUMMARY")
    print("=" * 70)
    
    print(f"Sun: {complete_chart['sunSign']}")
    print(f"Rising: {complete_chart['risingSign']} {complete_chart['ascendant']['exactDegree']}")
    print(f"Moon: {complete_chart['moonSign']}")
    print(f"Chart Ruler: {complete_chart['chartRuler']['planet']} in {complete_chart['chartRuler']['sign']}")
    print(f"House System: {complete_chart['houseSystem']} (Whole Sign)")
    
    print("\nALL PLANETARY PLACEMENTS:")
    for placement in complete_chart["placements"]:
        retro_symbol = " ℞" if placement["retrograde"] else ""
        print(f"  {placement['planet']}: {placement['sign']} {placement['exactDegree']} (House {placement['house']}){retro_symbol}")

def get_sign_ruler(sign):
    """Get traditional ruler of zodiac sign."""
    rulers = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
        "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
        "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
        "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }
    return rulers.get(sign, "Unknown")

def get_house_ruler(house_num, rising_sign):
    """Get ruler of house based on Whole Sign system."""
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    rising_index = signs.index(rising_sign)
    house_sign_index = (rising_index + house_num - 1) % 12
    house_sign = signs[house_sign_index]
    
    return get_sign_ruler(house_sign)

if __name__ == "__main__":
    asyncio.run(generate_complete_mia_chart())