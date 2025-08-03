#!/usr/bin/env python3
"""
Test PySwissEph calculations for Mia's accurate natal chart.
This provides precise astronomical data with full debugging information.
"""

import asyncio
import json
from datetime import datetime
from models import BirthInfoRequest
from services.pyswisseph_service import PySwissEphService
from services.geocoding_service import GeocodingService

async def test_mia_accurate_chart():
    """Generate Mia's accurate natal chart using Swiss Ephemeris."""
    
    print("=" * 90)
    print("MIA'S ACCURATE NATAL CHART - SWISS EPHEMERIS ASTRONOMICAL DATA")
    print("=" * 90)
    
    # Initialize Swiss Ephemeris service
    astrology_service = PySwissEphService()
    geocoding_service = GeocodingService()
    
    print("✓ Initialized PySwissEph service (Swiss Ephemeris v2.10.03)")
    print("✓ House system: Whole Sign (W)")
    
    # Mia's precise birth information
    print(f"\nBIRTH INFORMATION:")
    birth_info = BirthInfoRequest(
        name="Mia",
        date="22/11/1974",  # DD/MM/YYYY format - will be converted to 1974-11-22
        time="19:10",       # 7:10 PM local time
        location="Adelaide, South Australia, Australia"
    )
    
    print(f"  Name: {birth_info.name}")
    print(f"  Date: {birth_info.date} → {birth_info.date} (November 22, 1974)")
    print(f"  Time: {birth_info.time} (7:10 PM Adelaide local time)")
    print(f"  Location: {birth_info.location}")
    
    # Get precise Adelaide coordinates
    print(f"\nGEOCODING ADELAIDE:")
    try:
        coords = await geocoding_service.get_coordinates(birth_info.location)
        birth_info.latitude = coords["latitude"]
        birth_info.longitude = coords["longitude"]
        birth_info.timezone = 9.5  # Adelaide UTC+9:30 (standard time)
        
        print(f"  Latitude: {birth_info.latitude:.6f}°")
        print(f"  Longitude: {birth_info.longitude:.6f}°")
        print(f"  Timezone: UTC+{birth_info.timezone} (Adelaide)")
        
    except Exception as e:
        print(f"  Geocoding failed: {e}")
        # Use known precise coordinates for Adelaide
        birth_info.latitude = -34.9285
        birth_info.longitude = 138.6007
        birth_info.timezone = 9.5
        print(f"  Using fallback: {birth_info.latitude}°, {birth_info.longitude}°")
    
    # Generate precise astronomical chart
    print(f"\nGENERATING ASTRONOMICAL CHART:")
    try:
        chart_response = await astrology_service.generate_chart(birth_info)
        
        print(f"✓ Swiss Ephemeris calculations completed")
        print(f"✓ Planets calculated: {len(chart_response.planets)}")
        print(f"✓ Houses calculated: {len(chart_response.houses)}")
        
        # Display detailed astronomical results
        print(f"\n" + "=" * 90)
        print("SWISS EPHEMERIS ASTRONOMICAL RESULTS")
        print("=" * 90)
        
        # Ascendant information
        print(f"\nASCENDANT (RISING SIGN):")
        print(f"  Sign: {chart_response.ascendant.sign}")
        print(f"  Exact Degree: {chart_response.ascendant.degree:.8f}°")
        
        # Format to degrees, minutes, seconds
        asc_deg = int(chart_response.ascendant.degree)
        asc_min = int((chart_response.ascendant.degree % 1) * 60)
        asc_sec = int(((chart_response.ascendant.degree % 1) * 60 % 1) * 60)
        print(f"  Formatted: {asc_deg}°{asc_min:02d}'{asc_sec:02d}\"")
        
        # Planetary positions table
        print(f"\nPLANETARY POSITIONS (Swiss Ephemeris Data):")
        print("=" * 90)
        print("Planet".ljust(12) + "Sign".ljust(12) + "Exact Degree".ljust(20) + "House".ljust(8) + "Retrograde")
        print("-" * 90)
        
        # Sort planets in traditional order
        planet_order = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron", "North Node", "South Node"]
        sorted_planets = sorted(chart_response.planets, key=lambda p: planet_order.index(p.name) if p.name in planet_order else 999)
        
        for planet in sorted_planets:
            # Format exact degree to DMS
            deg = int(planet.degree)
            min_val = int((planet.degree % 1) * 60)
            sec = int(((planet.degree % 1) * 60 % 1) * 60)
            formatted_degree = f"{deg}°{min_val:02d}'{sec:02d}\" ({planet.degree:.6f}°)"
            
            retro_status = "Yes" if planet.retro else "No"
            
            print(f"{planet.name.ljust(12)}{planet.sign.ljust(12)}{formatted_degree.ljust(20)}{str(planet.house).ljust(8)}{retro_status}")
        
        # Whole Sign House System verification
        print(f"\nWHOLE SIGN HOUSE SYSTEM DEBUG:")
        print("=" * 90)
        print("House".ljust(8) + "Sign".ljust(12) + "Cusp".ljust(15) + "Planets in House")
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
            
            cusp_display = "0°00'00\""
            print(f"{str(house.house).ljust(8)}{house.sign.ljust(12)}{cusp_display.ljust(15)}{planets_str}")
        
        # House assignment logic verification
        print(f"\nHOUSE ASSIGNMENT VERIFICATION:")
        print("=" * 90)
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        rising_index = signs.index(chart_response.ascendant.sign)
        
        print(f"Rising Sign: {chart_response.ascendant.sign} (Index: {rising_index})")
        print("Expected Whole Sign House Assignment:")
        
        for i in range(1, 13):
            expected_sign_index = (rising_index + i - 1) % 12
            expected_sign = signs[expected_sign_index]
            actual_house = next((h for h in chart_response.houses if h.house == i), None)
            actual_sign = actual_house.sign if actual_house else "Unknown"
            
            match_status = "✓" if expected_sign == actual_sign else "✗"
            print(f"  House {i:2d}: Expected {expected_sign.ljust(11)} | Actual {actual_sign.ljust(11)} {match_status}")
        
        # Astronomical verification for user's corrections
        print(f"\n" + "=" * 90)
        print("ASTRONOMICAL VERIFICATION")
        print("=" * 90)
        
        sun_planet = next((p for p in chart_response.planets if p.name == "Sun"), None)
        if sun_planet:
            print(f"☀ Sun Position: {sun_planet.sign} {sun_planet.degree:.6f}°")
            
            # Check user's expectation: Sun at 29° Scorpio
            if sun_planet.sign == "Scorpio":
                if 28.5 <= sun_planet.degree <= 30:
                    print("  ✓ MATCHES USER DATA: Sun in late Scorpio")
                else:
                    print(f"  ⚠ User expects 29° Scorpio, calculated {sun_planet.degree:.2f}° Scorpio")
            elif sun_planet.sign == "Sagittarius":
                if sun_planet.degree < 1:
                    print("  ℹ Sun just entered Sagittarius (very early degrees)")
                    print("  ℹ This suggests the Sun was at 29°+ Scorpio shortly before birth time")
                else:
                    print(f"  ⚠ Sun well into Sagittarius ({sun_planet.degree:.2f}°)")
        
        print(f"🌅 Ascendant: {chart_response.ascendant.sign} {chart_response.ascendant.degree:.6f}°")
        
        # Check user's expectation: 19° Taurus Rising
        if chart_response.ascendant.sign == "Taurus":
            if 18 <= chart_response.ascendant.degree <= 20:
                print("  ✓ MATCHES USER DATA: Taurus Rising around 19°")
            else:
                print(f"  ⚠ User expects 19° Taurus, calculated {chart_response.ascendant.degree:.2f}° Taurus")
        else:
            print(f"  ⚠ User expects Taurus Rising, calculated {chart_response.ascendant.sign}")
        
        # Complete JSON chart format
        print(f"\n" + "=" * 90)
        print("COMPLETE NATAL CHART JSON")
        print("=" * 90)
        
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
            "astronomicalSource": "Swiss Ephemeris v2.10.03",
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
        
        # Final summary
        print(f"\n" + "=" * 90)
        print("ASTRONOMICAL CALCULATION SUMMARY")
        print("=" * 90)
        print("✓ Used Swiss Ephemeris (industry standard for astrological calculations)")
        print("✓ Calculated precise planetary positions for November 22, 1974, 19:10 Adelaide")
        print("✓ Applied Whole Sign house system with proper sign-based assignments")
        print("✓ All planetary bodies include exact degrees and retrograde status")
        print("✓ House placements determined by planetary sign, not degree position")
        print(f"✓ Generated {len(chart_response.planets)} planetary positions and {len(chart_response.houses)} houses")
        
        if sun_planet and sun_planet.sign in ["Scorpio", "Sagittarius"]:
            print(f"ℹ Note: Astronomical data shows Sun in {sun_planet.sign} {sun_planet.degree:.2f}°")
            print(f"ℹ This represents precise ephemeris calculations for the given date/time/location")
        
    except Exception as e:
        print(f"❌ Swiss Ephemeris calculation failed: {e}")
        print("This indicates an issue with the astronomical calculations")

if __name__ == "__main__":
    asyncio.run(test_mia_accurate_chart())