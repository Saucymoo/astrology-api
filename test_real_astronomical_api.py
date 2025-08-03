#!/usr/bin/env python3
"""
Test real astronomical API with Swiss Ephemeris data for Mia's chart.
Provides debugging information for planetary positions and house assignments.
"""

import asyncio
import json
import os
from datetime import datetime
from models import BirthInfoRequest
from services.astrology_service import AstrologyService
from services.geocoding_service import GeocodingService

async def test_real_astronomical_data():
    """Test real astronomical API with Mia's birth data."""
    
    print("=" * 80)
    print("TESTING REAL ASTRONOMICAL API - SWISS EPHEMERIS DATA")
    print("=" * 80)
    
    # Check API key
    api_key = os.getenv("FREE_ASTROLOGY_API_KEY")
    if not api_key:
        print("❌ ERROR: FREE_ASTROLOGY_API_KEY not found in environment variables")
        return
    else:
        print(f"✅ FREE_ASTROLOGY_API_KEY found: {api_key[:10]}...")
    
    # Initialize services
    print("\n🔧 Initializing real astronomical services...")
    astrology_service = AstrologyService()
    astrology_service.set_house_system("W")  # Whole Sign Houses
    geocoding_service = GeocodingService()
    
    print(f"📡 API Base URL: {astrology_service.base_url}")
    print(f"🏠 House System: {astrology_service.get_house_system()} (Whole Sign)")
    
    # Mia's birth information
    print("\n📅 Birth Information:")
    birth_info = BirthInfoRequest(
        name="Mia",
        date="22/11/1974",  # DD/MM/YYYY format
        time="19:10",
        location="Adelaide, South Australia, Australia"
    )
    
    print(f"  Name: {birth_info.name}")
    print(f"  Date: {birth_info.date} → {birth_info.date} (November 22, 1974)")
    print(f"  Time: {birth_info.time} (7:10 PM)")
    print(f"  Location: {birth_info.location}")
    
    # Get coordinates for Adelaide
    print(f"\n🌍 Geocoding location...")
    try:
        coords = await geocoding_service.get_coordinates(birth_info.location)
        birth_info.latitude = coords["latitude"]
        birth_info.longitude = coords["longitude"]
        birth_info.timezone = 9.5  # Adelaide UTC+9:30 (but in 1974 it was UTC+9:30)
        
        print(f"  Latitude: {birth_info.latitude}")
        print(f"  Longitude: {birth_info.longitude}")
        print(f"  Timezone: UTC+{birth_info.timezone}")
        
    except Exception as e:
        print(f"⚠️  Geocoding failed: {e}")
        # Use known Adelaide coordinates
        birth_info.latitude = -34.9285
        birth_info.longitude = 138.6007
        birth_info.timezone = 9.5
        print(f"  Using fallback coordinates: {birth_info.latitude}, {birth_info.longitude}")
    
    # Generate chart using real astronomical API
    print(f"\n🔮 Calling real astronomical API...")
    try:
        chart_response = await astrology_service.generate_chart(birth_info)
        
        print(f"✅ Successfully received astronomical data from Swiss Ephemeris")
        print(f"📊 Planets received: {len(chart_response.planets)}")
        print(f"🏠 Houses received: {len(chart_response.houses)}")
        
        # Display astronomical results
        print(f"\n" + "=" * 80)
        print("REAL ASTRONOMICAL DATA - SWISS EPHEMERIS RESULTS")
        print("=" * 80)
        
        print(f"\n🌅 ASCENDANT (RISING SIGN):")
        print(f"  Sign: {chart_response.ascendant.sign}")
        print(f"  Exact Degree: {chart_response.ascendant.degree:.6f}°")
        exact_deg = int(chart_response.ascendant.degree)
        exact_min = int((chart_response.ascendant.degree % 1) * 60)
        exact_sec = int(((chart_response.ascendant.degree % 1) * 60 % 1) * 60)
        print(f"  Formatted: {exact_deg}°{exact_min:02d}'{exact_sec:02d}\"")
        
        print(f"\n☀️ PLANETARY POSITIONS (Swiss Ephemeris Data):")
        print("Planet".ljust(12) + "Sign".ljust(12) + "Exact Degree".ljust(15) + "House".ljust(8) + "Retrograde")
        print("-" * 65)
        
        for planet in sorted(chart_response.planets, key=lambda p: ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron", "North Node", "South Node"].index(p.name) if p.name in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron", "North Node", "South Node"] else 999):
            
            # Format exact degree
            deg = int(planet.degree)
            min_val = int((planet.degree % 1) * 60)
            sec = int(((planet.degree % 1) * 60 % 1) * 60)
            formatted_degree = f"{deg}°{min_val:02d}'{sec:02d}\""
            
            retro_symbol = "Yes" if planet.retro else "No"
            
            print(f"{planet.name.ljust(12)}{planet.sign.ljust(12)}{formatted_degree.ljust(15)}{str(planet.house).ljust(8)}{retro_symbol}")
        
        print(f"\n🏠 WHOLE SIGN HOUSE SYSTEM DEBUG:")
        print("House".ljust(8) + "Sign".ljust(12) + "Cusp Degree".ljust(15) + "Planets in House")
        print("-" * 60)
        
        # Group planets by house
        planets_by_house = {}
        for planet in chart_response.planets:
            if planet.house not in planets_by_house:
                planets_by_house[planet.house] = []
            planets_by_house[planet.house].append(planet.name)
        
        for house in sorted(chart_response.houses, key=lambda h: h.house):
            planets_in_house = planets_by_house.get(house.house, [])
            planets_str = ", ".join(planets_in_house) if planets_in_house else "Empty"
            
            # Format house cusp degree
            deg = int(house.degree)
            min_val = int((house.degree % 1) * 60)
            sec = int(((house.degree % 1) * 60 % 1) * 60)
            formatted_degree = f"{deg}°{min_val:02d}'{sec:02d}\""
            
            print(f"{str(house.house).ljust(8)}{house.sign.ljust(12)}{formatted_degree.ljust(15)}{planets_str}")
        
        # Whole Sign House Assignment Logic Check
        print(f"\n🔍 WHOLE SIGN HOUSE ASSIGNMENT VERIFICATION:")
        print(f"Rising Sign: {chart_response.ascendant.sign} → House 1")
        
        # Calculate expected house signs using Whole Sign logic
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        rising_index = signs.index(chart_response.ascendant.sign)
        
        print("Expected Whole Sign House Assignment:")
        for i in range(1, 13):
            house_sign_index = (rising_index + i - 1) % 12
            expected_sign = signs[house_sign_index]
            actual_house = next((h for h in chart_response.houses if h.house == i), None)
            actual_sign = actual_house.sign if actual_house else "Unknown"
            
            match_status = "✅" if expected_sign == actual_sign else "❌"
            print(f"  House {i:2d}: Expected {expected_sign.ljust(11)} | Actual {actual_sign.ljust(11)} {match_status}")
        
        # Key astronomical confirmations
        print(f"\n" + "=" * 80)
        print("ASTRONOMICAL CONFIRMATIONS FOR MIA'S CHART")
        print("=" * 80)
        
        sun_planet = next((p for p in chart_response.planets if p.name == "Sun"), None)
        if sun_planet:
            print(f"☀️  Sun: {sun_planet.sign} {sun_planet.degree:.2f}° (Should be ~29° Scorpio for Nov 22, 1974)")
            
        print(f"🌅 Ascendant: {chart_response.ascendant.sign} {chart_response.ascendant.degree:.2f}° (Should be ~19° Taurus)")
        
        # JSON output for API testing
        print(f"\n" + "=" * 80)
        print("COMPLETE JSON FOR API RESPONSE")
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
            "ascendant": {
                "sign": chart_response.ascendant.sign,
                "degree": chart_response.ascendant.degree,
                "exactDegree": f"{exact_deg}°{exact_min:02d}'{exact_sec:02d}\""
            },
            "placements": []
        }
        
        for planet in chart_response.planets:
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
        
    except Exception as e:
        print(f"❌ Astronomical API call failed: {e}")
        print(f"🔧 This could be due to:")
        print(f"   - API authentication issues")
        print(f"   - Network connectivity")
        print(f"   - API service unavailable")
        print(f"   - Invalid request format")

if __name__ == "__main__":
    asyncio.run(test_real_astronomical_data())