#!/usr/bin/env python3
"""
Test script to diagnose why external API might return Placidus instead of Whole Sign.
This will test the actual API payload being sent and verify the response.
"""

import asyncio
import json
import requests
from models import BirthInfoRequest

async def test_external_api_house_system():
    """Test external API directly to see what house system is being used."""
    
    print("EXTERNAL API HOUSE SYSTEM DIAGNOSIS")
    print("=" * 60)
    
    # Test data
    birth_info = BirthInfoRequest(
        name="Test User",
        date="1990-06-15", 
        time="14:30",
        location="New York, NY, USA",
        latitude=40.7127281,
        longitude=-74.0060152,
        timezone=-5
    )
    
    # Parse birth info for API
    date_parts = birth_info.date.split('-')
    time_parts = birth_info.time.split(':')
    
    year = int(date_parts[0])
    month = int(date_parts[1]) 
    day = int(date_parts[2])
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    
    # Test different house system configurations
    test_cases = [
        {"house_system": "W", "name": "Whole Sign"},
        {"house_system": "P", "name": "Placidus"},
        {"house_system": None, "name": "No house_system parameter"}
    ]
    
    base_url = "https://api.freeastrologyapi.com/api/v1"
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print("-" * 40)
        
        # Prepare payload
        payload = {
            "day": day,
            "month": month, 
            "year": year,
            "hour": hour,
            "min": minute,
            "lat": birth_info.latitude,
            "lon": birth_info.longitude,
            "tzone": birth_info.timezone or 0
        }
        
        # Add house system if specified
        if test_case["house_system"]:
            payload["house_system"] = test_case["house_system"]
        
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(
                f"{base_url}/birth-chart",
                json=payload,
                timeout=30,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Astrology-Chart-API/1.0"
                }
            )
            
            if response.ok:
                data = response.json()
                
                # Analyze houses in response
                houses = data.get("houses", [])
                if houses:
                    print(f"✓ Response received with {len(houses)} houses")
                    print("House analysis:")
                    
                    zero_degree_count = 0
                    for house in houses[:6]:  # Show first 6 houses
                        degree = house.get("degree", 0)
                        if degree == 0.0:
                            zero_degree_count += 1
                        print(f"  House {house.get('house', '?')}: {house.get('sign', '?')} at {degree}°")
                    
                    # Detect likely system
                    if zero_degree_count >= 5:
                        detected = "Likely Whole Sign (many 0° cusps)"
                    elif zero_degree_count == 0:
                        detected = "Likely Placidus (no 0° cusps)" 
                    else:
                        detected = "Mixed/Unclear"
                    
                    print(f"Detection: {detected}")
                else:
                    print("⚠ No houses in response")
                    
            else:
                print(f"✗ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"✗ Request failed: {str(e)}")
    
    print(f"\n" + "=" * 60)
    print("DIAGNOSIS SUMMARY:")
    print("=" * 60)
    print("1. If external API ignores house_system parameter:")
    print("   → API always returns Placidus regardless of parameter")
    print("   → Need to find different API or implement local calculations")
    print("\n2. If external API respects house_system='W':")
    print("   → Should see houses at 0° degrees for Whole Sign")
    print("   → Problem might be elsewhere in the code")
    print("\n3. Current code configuration:")
    print("   → services/astrology_service.py sets house_system='W'")
    print("   → This parameter is sent in API payload")
    print("   → Mock service correctly implements Whole Sign")

if __name__ == "__main__":
    asyncio.run(test_external_api_house_system())