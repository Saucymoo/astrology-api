#!/usr/bin/env python3
"""
Generate results from both Swiss Ephemeris and external API attempts
for user verification of astronomical accuracy.
"""

import asyncio
import json
import httpx
from datetime import datetime
from models import BirthInfoRequest
from services.astrology_calculations import AstrologyCalculationsService

async def get_swiss_ephemeris_results():
    """Get actual Swiss Ephemeris calculations."""
    print("=" * 70)
    print("SWISS EPHEMERIS RESULTS")
    print("=" * 70)
    
    birth_info = BirthInfoRequest(
        name="Accuracy Test",
        date="22/11/1974",
        time="19:10",
        location="Adelaide, Australia",
        latitude=-34.9285,
        longitude=138.6007,
        timezone=9.5
    )
    
    try:
        astrology_service = AstrologyCalculationsService()
        astrology_service.set_house_system("W")
        
        raw_chart = await astrology_service.generate_chart(birth_info)
        
        # Format results for comparison
        results = {
            "source": "Swiss Ephemeris v2.10.03",
            "birth_data": {
                "date": "November 22, 1974",
                "time": "19:10 (7:10 PM)",
                "location": "Adelaide, Australia",
                "coordinates": {
                    "latitude": -34.9285,
                    "longitude": 138.6007,
                    "timezone": "UTC+9.5"
                }
            },
            "house_system": "Whole Signs",
            "ascendant": {
                "sign": raw_chart.ascendant.sign,
                "degree": raw_chart.ascendant.degree,
                "exact_degree": f"{int(raw_chart.ascendant.degree)}°{int((raw_chart.ascendant.degree % 1) * 60):02d}'{int(((raw_chart.ascendant.degree % 1) * 60 % 1) * 60):02d}\""
            },
            "planets": []
        }
        
        # Get all planetary positions
        for planet in raw_chart.planets:
            planet_data = {
                "name": planet.name,
                "sign": planet.sign,
                "degree": planet.degree,
                "house": planet.house,
                "exact_degree": f"{int(planet.degree)}°{int((planet.degree % 1) * 60):02d}'{int(((planet.degree % 1) * 60 % 1) * 60):02d}\"",
                "retrograde": getattr(planet, 'retrograde', False)
            }
            results["planets"].append(planet_data)
        
        # Display formatted results
        print(f"Birth Data: {results['birth_data']['date']} at {results['birth_data']['time']}")
        print(f"Location: {results['birth_data']['location']}")
        print(f"Coordinates: {results['birth_data']['coordinates']['latitude']}, {results['birth_data']['coordinates']['longitude']}")
        print(f"Timezone: {results['birth_data']['coordinates']['timezone']}")
        print(f"House System: {results['house_system']}")
        print()
        print(f"ASCENDANT: {results['ascendant']['sign']} {results['ascendant']['exact_degree']}")
        print()
        print("PLANETARY POSITIONS:")
        print("Planet".ljust(12) + "Sign".ljust(12) + "Exact Degree".ljust(13) + "House".ljust(6) + "Retrograde")
        print("-" * 65)
        
        for planet in results["planets"]:
            retro = "Yes" if planet.get("retrograde", False) else "No"
            print(f"{planet['name'].ljust(12)}{planet['sign'].ljust(12)}{planet['exact_degree'].ljust(13)}{str(planet['house']).ljust(6)}{retro}")
        
        print(f"\nTotal Planets Calculated: {len(results['planets'])}")
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return None

async def attempt_external_api_calls():
    """Attempt to get data from external APIs for comparison."""
    print(f"\n" + "=" * 70)
    print("EXTERNAL API ATTEMPTS")
    print("=" * 70)
    
    test_data = {
        "date": "1974-11-22",
        "time": "19:10",
        "latitude": -34.9285,
        "longitude": 138.6007,
        "timezone": 9.5,
        "house_system": "W"
    }
    
    # APIs to test
    apis = [
        {
            "name": "Free Astrology API",
            "url": "https://freeastrologyapi.com/api/houses",
            "method": "POST"
        },
        {
            "name": "Free Astrology API (Chart)",
            "url": "https://freeastrologyapi.com/api/chart",
            "method": "POST"
        },
        {
            "name": "Free Astrology API (Planets)",
            "url": "https://freeastrologyapi.com/api/planets",
            "method": "POST"
        }
    ]
    
    results = {
        "source": "External APIs",
        "test_data": test_data,
        "api_responses": []
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for api in apis:
            print(f"\nTesting: {api['name']}")
            print(f"URL: {api['url']}")
            print(f"Data sent: {json.dumps(test_data, indent=2)}")
            
            try:
                response = await client.post(
                    api['url'],
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                )
                
                api_result = {
                    "name": api['name'],
                    "url": api['url'],
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "response_text": response.text[:500] if response.text else None
                }
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        api_result["json_data"] = data
                        print("✅ SUCCESS - JSON data received")
                        print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dictionary'}")
                        
                        # Look for planetary data
                        if isinstance(data, dict):
                            for key in ['planets', 'sun', 'moon', 'ascendant', 'houses', 'chart']:
                                if key in data:
                                    print(f"Found {key}: {type(data[key])}")
                    except json.JSONDecodeError:
                        print("Response is not valid JSON")
                        api_result["error"] = "Invalid JSON response"
                
                elif response.status_code == 404:
                    print("❌ API endpoint not found (404)")
                    api_result["error"] = "Endpoint not found"
                
                elif response.status_code == 401 or response.status_code == 403:
                    print("❌ Authentication required")
                    api_result["error"] = "Authentication required"
                
                else:
                    print(f"❌ Error {response.status_code}")
                    print(f"Response: {response.text[:200]}")
                    api_result["error"] = f"HTTP {response.status_code}"
                
                results["api_responses"].append(api_result)
                
            except Exception as e:
                print(f"❌ Connection failed: {e}")
                results["api_responses"].append({
                    "name": api['name'],
                    "url": api['url'],
                    "error": str(e)
                })
    
    return results

async def generate_comparison_for_user():
    """Generate comprehensive comparison for user verification."""
    
    print("Generating comparison data for user verification...")
    print("This will show you the actual results from both approaches.")
    
    # Get Swiss Ephemeris results
    swiss_results = await get_swiss_ephemeris_results()
    
    # Attempt external API calls  
    api_results = await attempt_external_api_calls()
    
    # Create comprehensive comparison
    comparison = {
        "test_info": {
            "date": "November 22, 1974",
            "time": "19:10 (7:10 PM)",
            "location": "Adelaide, Australia", 
            "coordinates": {
                "latitude": -34.9285,
                "longitude": 138.6007,
                "timezone": "UTC+9.5"
            },
            "requested_house_system": "Whole Signs"
        },
        "swiss_ephemeris_results": swiss_results,
        "external_api_results": api_results,
        "comparison_notes": {
            "user_verification": "User previously confirmed Sun at 29°42'23\" Scorpio is astronomically correct",
            "purpose": "Compare both approaches for astronomical accuracy verification"
        }
    }
    
    # Save detailed comparison
    with open('complete_api_test.json', 'w') as f:
        json.dump(comparison, f, indent=2)
    
    print(f"\n" + "=" * 70)
    print("SUMMARY FOR USER VERIFICATION")
    print("=" * 70)
    
    if swiss_results:
        sun_planet = next((p for p in swiss_results['planets'] if p['name'] == 'Sun'), None)
        if sun_planet:
            print(f"SWISS EPHEMERIS Sun Position: {sun_planet['sign']} {sun_planet['exact_degree']}")
            print(f"Your Previous Correction: Sun at 29°42'23\" Scorpio")
            
            # Check if they match
            if sun_planet['sign'] == 'Scorpio' and '29°42' in sun_planet['exact_degree']:
                print("✅ MATCH: Swiss Ephemeris matches your astronomical correction")
            else:
                print("⚠ DIFFERENCE: Please verify which is more accurate")
    
    working_apis = [r for r in api_results['api_responses'] if r.get('status_code') == 200]
    if working_apis:
        print(f"\nEXTERNAL APIs: {len(working_apis)} working API(s) found")
        for api in working_apis:
            print(f"✅ {api['name']}: Data available for comparison")
    else:
        print(f"\nEXTERNAL APIs: No working APIs found")
        failed_apis = [r for r in api_results['api_responses'] if 'error' in r]
        for api in failed_apis:
            print(f"❌ {api['name']}: {api.get('error', 'Failed')}")
    
    print(f"\n✅ Complete comparison saved to: complete_api_test.json")
    print("You can now review both sets of results for accuracy verification.")
    
    return comparison

if __name__ == "__main__":
    result = asyncio.run(generate_comparison_for_user())