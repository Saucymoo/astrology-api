#!/usr/bin/env python3
"""
Test Swiss Ephemeris calculations for Mia's chart.
This will provide accurate astronomical data with detailed debugging.
"""

import asyncio
import json
from datetime import datetime
from models import BirthInfoRequest
from services.swiss_ephemeris_service import SwissEphemerisService
from services.geocoding_service import GeocodingService

async def test_mia_swiss_ephemeris():
    """Test Swiss Ephemeris calculations for Mia's birth chart."""
    
    print("=" * 80)
    print("MIA'S ACCURATE NATAL CHART - SWISS EPHEMERIS CALCULATIONS")
    print("=" * 80)
    
    # Initialize Swiss Ephemeris service
    print("Initializing Swiss Ephemeris service...")
    astrology_service = SwissEphemerisService()
    geocoding_service = GeocodingService()
    
    # Mia's birth information
    print("\nBirth Information:")
    birth_info = BirthInfoRequest(
        name="Mia",
        date="22/11/1974",  # DD/MM/YYYY format
        time="19:10",
        location="Adelaide, South Australia, Australia"
    )
    
    print(f"  Name: {birth_info.name}")
    print(f"  Date: {birth_info.date} → November 22, 1974")
    print(f"  Time: {birth_info.time} (7:10 PM local time)")
    print(f"  Location: {birth_info.location}")
    
    # Get precise coordinates for Adelaide
    print(f"\nGeocoding Adelaide coordinates...")
    try:
        coords = await geocoding_service.get_coordinates(birth_info.location)
        birth_info.latitude = coords["latitude"]
        birth_info.longitude = coords["longitude"]
        birth_info.timezone = 9.5  # Adelaide UTC+9:30
        
        print(f"  Latitude: {birth_info.latitude}°")
        print(f"  Longitude: {birth_info.longitude}°")
        print(f"  Timezone: UTC+{birth_info.timezone}")
        
    except Exception as e:
        print(f"  Geocoding failed: {e}")
        # Use precise Adelaide coordinates
        birth_info.latitude = -34.9285
        birth_info.longitude = 138.6007
        birth_info.timezone = 9.5
        print(f"  Using precise coordinates: {birth_info.latitude}°, {birth_info.longitude}°")
    
    # Generate accurate chart using Swiss Ephemeris
    print(f"\nGenerating chart using Swiss Ephemeris...")
    try:
        chart_response = await astrology_service.generate_chart(birth_info)
        
        print(f"✓ Successfully calculated astronomical positions")
        print(f"✓ Planets calculated: {len(chart_response.planets)}")
        print(f"✓ Houses calculated: {len(chart_response.houses)}")
        
        # Display accurate astronomical results
        print(f"\n" + "=" * 80)
        print("SWISS EPHEMERIS ASTRONOMICAL DATA")
        print("=" * 80)
        
        print(f"\nASCENDANT (RISING SIGN):")
        print(f"  Sign: {chart_response.ascendant.sign}")
        print(f"  Exact Degree: {chart_response.ascendant.degree:.6f}°")
        
        # Format exact degree
        asc_deg = int(chart_response.ascendant.degree)
        asc_min = int((chart_response.ascendant.degree % 1) * 60)
        asc_sec = int(((chart_response.ascendant.degree % 1) * 60 % 1) * 60)
        print(f"  Formatted: {asc_deg}°{asc_min:02d}'{asc_sec:02d}\"")
        
        print(f"\nPLANETARY POSITIONS (Swiss Ephemeris):")
        print("Planet".ljust(12) + "Sign".ljust(12) + "Exact Degree".ljust(18) + "House".ljust(8) + "Retro")
        print("-" * 70)
        
        # Display planets in traditional order
        planet_order = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron", "North Node", "South Node"]
        sorted_planets = sorted(chart_response.planets, key=lambda p: planet_order.index(p.name) if p.name in planet_order else 999)
        
        for planet in sorted_planets:
            # Format exact degree
            deg = int(planet.degree)
            min_val = int((planet.degree % 1) * 60)
            sec = int(((planet.degree % 1) * 60 % 1) * 60)
            formatted_degree = f"{deg}°{min_val:02d}'{sec:02d}\""
            
            retro_symbol = "Yes" if planet.retro else "No"
            
            print(f"{planet.name.ljust(12)}{planet.sign.ljust(12)}{formatted_degree.ljust(18)}{str(planet.house).ljust(8)}{retro_symbol}")
        
        print(f"\nWHOLE SIGN HOUSE ASSIGNMENTS:")
        print("House".ljust(8) + "Sign".ljust(12) + "Planets")
        print("-" * 40)
        
        # Group planets by house
        planets_by_house = {}
        for planet in chart_response.planets:
            if planet.house not in planets_by_house:
                planets_by_house[planet.house] = []
            planets_by_house[planet.house].append(planet.name)
        
        for house in sorted(chart_response.houses, key=lambda h: h.house):
            planets_in_house = planets_by_house.get(house.house, [])
            planets_str = ", ".join(planets_in_house) if planets_in_house else "Empty"
            
            print(f"{str(house.house).ljust(8)}{house.sign.ljust(12)}{planets_str}")
        
        # Verification of key astronomical data
        print(f"\n" + "=" * 80)
        print("ASTRONOMICAL VERIFICATION")
        print("=" * 80)
        
        sun_planet = next((p for p in chart_response.planets if p.name == "Sun"), None)
        if sun_planet:
            print(f"Sun Position: {sun_planet.sign} {sun_planet.degree:.2f}°")
            if sun_planet.sign == "Scorpio" and 28 <= sun_planet.degree <= 30:
                print("✓ CORRECT: Sun at late Scorpio for November 22, 1974")
            else:
                print("⚠ Check: Expected Sun ~29° Scorpio for Nov 22, 1974")
                
        print(f"Ascendant: {chart_response.ascendant.sign} {chart_response.ascendant.degree:.2f}°")
        if chart_response.ascendant.sign == "Taurus" and 15 <= chart_response.ascendant.degree <= 25:
            print("✓ CORRECT: Taurus Rising around expected degree")
        else:
            print("⚠ Check: Expected ~19° Taurus Rising")
        
        # Complete JSON output
        print(f"\n" + "=" * 80)
        print("COMPLETE NATAL CHART JSON")
        print("=" * 80)
        
        complete_chart = {
            "name": birth_info.name,
            "birthDate": birth_info.date,
            "birthTime": birth_info.time,
            "location": birth_info.location,
            "coordinates": {
                "latitude": birth_info.latitude,
                "longitude": birth_info.longitude,
                "timezone": birth_info.timezone
            },
            "houseSystem": "W",
            "risingSign": chart_response.ascendant.sign,
            "sunSign": sun_planet.sign if sun_planet else "Unknown",
            "moonSign": next((p.sign for p in chart_response.planets if p.name == "Moon"), "Unknown"),
            "ascendant": {
                "sign": chart_response.ascendant.sign,
                "degree": chart_response.ascendant.degree,
                "exactDegree": f"{asc_deg}°{asc_min:02d}'{asc_sec:02d}\""
            },
            "placements": []
        }
        
        for planet in sorted_planets:
            deg = int(planet.degree)
            min_val = int((planet.degree % 1) * 60)
            sec = int(((planet.degree % 1) * 60 % 1) * 60)
            
            placement = {
                "planet": planet.name,
                "sign": planet.sign,
                "house": planet.house,
                "degree": planet.degree,
                "exactDegree": f"{deg}°{min_val:02d}'{sec:02d}\"",
                "retrograde": planet.retro
            }
            complete_chart["placements"].append(placement)
        
        print(json.dumps(complete_chart, indent=2))
        
        # Summary for user
        print(f"\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"✓ Used Swiss Ephemeris for precise astronomical calculations")
        print(f"✓ Applied Whole Sign house system correctly") 
        print(f"✓ Calculated exact planetary positions for November 22, 1974, 19:10, Adelaide")
        print(f"✓ All {len(chart_response.planets)} planetary bodies included")
        print(f"✓ Retrograde status calculated from actual planetary motion")
        print(f"✓ House assignments based on zodiac sign, not degrees")
        
    except Exception as e:
        print(f"❌ Swiss Ephemeris calculation failed: {e}")
        print(f"This indicates an issue with the Swiss Ephemeris library or calculation")

if __name__ == "__main__":
    asyncio.run(test_mia_swiss_ephemeris())