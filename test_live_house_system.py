#!/usr/bin/env python3
"""
Live API Test - Verify actual house system being used in production.
This will test the real API response to see if Whole Sign or Placidus is being used.
"""

import asyncio
import json
from services.astrology_service import AstrologyService
from services.geocoding_service import GeocodingService
from models import BirthInfoRequest

async def test_live_house_system():
    """Test what house system is actually being used by the live API."""
    
    print("LIVE API HOUSE SYSTEM TEST")
    print("=" * 60)
    
    # Initialize services (same as main.py)
    astrology_service = AstrologyService()
    geocoding_service = GeocodingService()
    
    print(f"1. Service Configuration:")
    print(f"   Configured house system: {astrology_service.house_system}")
    print(f"   Expected: 'W' (Whole Sign)")
    
    # Test birth info
    birth_info = BirthInfoRequest(
        name="House System Test",
        date="1990-06-15",
        time="14:30", 
        location="New York, NY, USA"
    )
    
    try:
        # Geocode location first (same as API does)
        print(f"\n2. Geocoding Test:")
        coords = await geocoding_service.get_coordinates(birth_info.location)
        print(f"   Location: {birth_info.location}")
        print(f"   Coordinates: {coords['latitude']}, {coords['longitude']}")
        
        # Update birth info with coordinates
        birth_info.latitude = coords['latitude']
        birth_info.longitude = coords['longitude']
        birth_info.timezone = coords.get('timezone', 0)
        
        print(f"\n3. Chart Generation Test:")
        print(f"   Calling astrology service...")
        print(f"   House system parameter: {astrology_service.house_system}")
        
        # Generate chart (this calls the real external API)
        chart = await astrology_service.generate_chart(birth_info)
        
        print(f"   Chart generated: {'✓' if chart.success else '✗'}")
        print(f"   Number of planets: {len(chart.planets)}")
        print(f"   Number of houses: {len(chart.houses)}")
        
        print(f"\n4. House System Analysis:")
        
        # Analyze house cusps to determine actual system
        house_degrees = [h.degree for h in chart.houses]
        zero_degree_count = sum(1 for degree in house_degrees if degree == 0.0)
        
        print(f"   Houses at exactly 0°: {zero_degree_count}/12")
        print(f"   Sample house cusps:")
        for i, house in enumerate(chart.houses[:6]):
            print(f"     House {house.house}: {house.sign} at {house.degree:.2f}°")
        
        # Determine likely house system
        if zero_degree_count >= 10:
            detected_system = "Whole Sign (W)"
            status = "✓ CORRECT"
        elif all(d != 0.0 for d in house_degrees):
            detected_system = "Placidus or other (P/K/O/etc.)"
            status = "✗ WRONG - Should be Whole Sign"
        else:
            detected_system = "Mixed/Unknown"
            status = "⚠ UNCLEAR"
        
        print(f"\n5. System Detection:")
        print(f"   Detected system: {detected_system}")
        print(f"   Status: {status}")
        
        print(f"\n6. API Payload Check:")
        print(f"   The API call should include: house_system='{astrology_service.house_system}'")
        print(f"   This is set in services/astrology_service.py line 116")
        
        return detected_system.startswith("Whole Sign")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print(f"   This might indicate API connectivity issues")
        print(f"   The external astrology API may be unavailable")
        return False

if __name__ == "__main__":
    asyncio.run(test_live_house_system())