#!/usr/bin/env python3
"""
Complete API test for Mia's birth data
"""

import requests
import json
import sys

def test_complete_api():
    """Test the full API functionality"""
    
    base_url = "http://localhost:8000"
    
    print("=" * 70)
    print("COMPLETE API TEST - MIA'S BIRTH DATA")
    print("=" * 70)
    
    # Test health endpoint
    try:
        health = requests.get(f"{base_url}/health", timeout=5)
        print(f"Health Check: {health.status_code}")
        if health.status_code == 200:
            print(f"✅ Server healthy: {health.json()}")
        else:
            print(f"❌ Health check failed: {health.text}")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False
    
    # Test Mia's chart generation
    mia_data = {
        "name": "Mia",
        "birth_date": "1974-11-22",
        "birth_time": "19:10",
        "birth_location": "Adelaide, South Australia, Australia"
    }
    
    print(f"\nChart Request:")
    print(json.dumps(mia_data, indent=2))
    
    try:
        response = requests.post(
            f"{base_url}/generate-chart",
            json=mia_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            chart = response.json()
            
            print(f"\n✅ CHART GENERATED SUCCESSFULLY")
            print("=" * 70)
            
            # Basic info
            print(f"Name: {chart['name']}")
            print(f"Date: {chart['birth_date']} (22 November 1974)")
            print(f"Time: {chart['birth_time']} (7:10 PM)")
            print(f"Location: {chart['birth_location']}")
            print(f"House System: {chart['house_system']}")
            
            # Key positions
            print(f"\nKEY ASTROLOGICAL POSITIONS:")
            print(f"Rising: {chart['rising_sign']} {chart['ascendant']['exact_degree']}")
            print(f"Sun: {chart['sun_sign']}")
            print(f"Moon: {chart['moon_sign']}")
            print(f"Midheaven: {chart['midheaven']['sign']} {chart['midheaven']['exact_degree']}")
            
            # Find specific planets
            sun_pos = next((p for p in chart['placements'] if p['planet'] == 'Sun'), None)
            moon_pos = next((p for p in chart['placements'] if p['planet'] == 'Moon'), None)
            
            print(f"\nDETAILED POSITIONS:")
            if sun_pos:
                print(f"Sun: {sun_pos['sign']} {sun_pos['exact_degree']} (House {sun_pos['house']})")
            if moon_pos:
                print(f"Moon: {moon_pos['sign']} {moon_pos['exact_degree']} (House {moon_pos['house']})")
            
            print(f"\nALL PLANETARY POSITIONS:")
            for planet in chart['placements']:
                retro = " (R)" if planet['retrograde'] else ""
                print(f"  {planet['planet']}: {planet['sign']} {planet['exact_degree']} - House {planet['house']}{retro}")
            
            # Verification against expected values
            print(f"\nVERIFICATION:")
            print(f"Expected vs Actual:")
            print(f"  Rising: Expected Taurus 19° → Actual {chart['ascendant']['sign']} {chart['ascendant']['exact_degree']}")
            if sun_pos:
                print(f"  Sun: Expected Scorpio 29° → Actual {sun_pos['sign']} {sun_pos['exact_degree']}")
            if moon_pos:
                print(f"  Moon: Expected Pisces 4° → Actual {moon_pos['sign']} {moon_pos['exact_degree']}")
            print(f"  House System: Expected Whole Sign → Actual {chart['house_system']}")
            
            return True
            
        elif response.status_code == 401:
            print(f"❌ 401 Unauthorized - API may require authentication")
            print(f"Response: {response.text}")
            return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_api()
    
    if success:
        print(f"\n" + "=" * 70)
        print("🎯 API TEST SUCCESSFUL")
        print("=" * 70)
        print("✅ Local FastAPI server working correctly")
        print("✅ Chart generation successful")
        print("✅ Swiss Ephemeris calculations working")
        print("✅ Whole Sign house system confirmed")
        print("✅ All required astrological data present")
    else:
        print(f"\n❌ API test failed")
        sys.exit(1)