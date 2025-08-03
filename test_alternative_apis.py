#!/usr/bin/env python3
"""
Test alternative astrology APIs to find working endpoints for comparison.
"""

import asyncio
import httpx
import json
from datetime import datetime

async def test_working_apis():
    """Test various astrology APIs that might be accessible."""
    
    print("=" * 80)
    print("TESTING ALTERNATIVE ASTROLOGY APIs")
    print("=" * 80)
    
    # Test data for Nov 22, 1974, 19:10, Adelaide
    test_data = {
        "date": "1974-11-22",
        "time": "19:10",
        "lat": -34.9285,
        "lon": 138.6007,
        "tz": 9.5
    }
    
    # Alternative formats
    test_data_alt = {
        "year": 1974,
        "month": 11,
        "day": 22,
        "hour": 19,
        "minute": 10,
        "latitude": -34.9285,
        "longitude": 138.6007,
        "timezone": 9.5
    }
    
    # List of potential working APIs
    apis = [
        {
            "name": "Astro-Seek (Free)",
            "url": "https://horoscope-api.astro-seek.com/calculate",
            "method": "GET"
        },
        {
            "name": "AstroAPI (Demo)",
            "url": "https://api.astroapi.com/demo/chart",
            "method": "POST"
        },
        {
            "name": "OpenAstro API",
            "url": "https://api.openastro.org/natal",
            "method": "POST"
        },
        {
            "name": "AstrologyAPI Demo",
            "url": "https://astrologyapi.com/api/demo/planets",
            "method": "POST"
        }
    ]
    
    results = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for api in apis:
            print(f"\nTesting: {api['name']}")
            print(f"URL: {api['url']}")
            
            try:
                if api['method'] == 'POST':
                    response = await client.post(
                        api['url'],
                        json=test_data,
                        headers={"Content-Type": "application/json"}
                    )
                else:
                    response = await client.get(
                        api['url'],
                        params=test_data
                    )
                
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print("✅ SUCCESS - JSON response received")
                        print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                        
                        # Look for planetary data
                        if isinstance(data, dict):
                            for key in ['planets', 'sun', 'positions', 'chart']:
                                if key in data:
                                    print(f"  Found {key}: {type(data[key])}")
                        
                        results.append({
                            "name": api['name'],
                            "url": api['url'],
                            "status": "working",
                            "data": data
                        })
                        
                    except json.JSONDecodeError:
                        print("⚠ Non-JSON response:")
                        print(response.text[:200])
                        
                elif response.status_code == 401:
                    print("❌ Authentication required")
                    results.append({
                        "name": api['name'],
                        "status": "auth_required"
                    })
                    
                elif response.status_code == 404:
                    print("❌ Endpoint not found")
                    
                else:
                    print(f"❌ Error {response.status_code}")
                    print(response.text[:200])
                    
            except httpx.ConnectError:
                print("❌ Connection failed - API not accessible")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    return results

async def create_comparison_chart():
    """Create a comparison of different calculation methods."""
    
    print(f"\n" + "=" * 80)
    print("CREATING COMPARISON CHART")
    print("=" * 80)
    
    # Our Swiss Ephemeris results (verified accurate)
    swiss_data = {
        "source": "Swiss Ephemeris (Our Implementation)",
        "sun": {"sign": "Scorpio", "degree": 29.706452, "exact": "29°42'23\""},
        "moon": {"sign": "Pisces", "degree": 4.70, "exact": "4°42'00\""},
        "ascendant": {"sign": "Gemini", "degree": 1.59, "exact": "1°35'22\""},
        "accuracy": "Verified by user - matches astronomical corrections"
    }
    
    # Test external APIs
    api_results = await test_working_apis()
    
    # Create comparison
    comparison = {
        "test_date": "1974-11-22 19:10 Adelaide",
        "coordinates": {"lat": -34.9285, "lon": 138.6007, "tz": 9.5},
        "methods": [swiss_data]
    }
    
    # Add any working API results
    for result in api_results:
        if result.get('status') == 'working' and 'data' in result:
            comparison["methods"].append({
                "source": result['name'],
                "data": result['data'],
                "status": "external_api"
            })
    
    return comparison

async def main():
    """Main comparison function."""
    
    comparison = await create_comparison_chart()
    
    print(f"\n" + "=" * 80)
    print("FINAL ACCURACY COMPARISON")
    print("=" * 80)
    
    print(f"Test Case: {comparison['test_date']}")
    print(f"Coordinates: {comparison['coordinates']}")
    print()
    
    for i, method in enumerate(comparison['methods'], 1):
        print(f"{i}. {method['source']}")
        
        if 'sun' in method:
            print(f"   Sun: {method['sun']['sign']} {method['sun']['exact']}")
            print(f"   Moon: {method['moon']['sign']} {method['moon']['exact']}")
            print(f"   Ascendant: {method['ascendant']['sign']} {method['ascendant']['exact']}")
            
            if 'accuracy' in method:
                print(f"   ✅ {method['accuracy']}")
        else:
            print(f"   Status: {method.get('status', 'Unknown')}")
            if 'data' in method:
                print(f"   Data available for detailed comparison")
    
    print(f"\n" + "=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    
    working_apis = [m for m in comparison['methods'] if m.get('status') == 'external_api']
    
    if working_apis:
        print(f"Found {len(working_apis)} working external API(s) for comparison")
        print("Recommend detailed comparison of planetary positions")
    else:
        print("No accessible external APIs found for comparison")
        print("Swiss Ephemeris remains the verified accurate source")
        print("✅ RECOMMENDATION: Continue with Swiss Ephemeris implementation")
        print("   - User-verified astronomical accuracy")
        print("   - No external dependencies")
        print("   - Reliable offline calculations")
    
    # Save results
    with open('accuracy_comparison_results.json', 'w') as f:
        json.dump(comparison, f, indent=2)
    
    print(f"\n✅ Comparison results saved to accuracy_comparison_results.json")

if __name__ == "__main__":
    asyncio.run(main())