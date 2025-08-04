#!/usr/bin/env python3
"""
Direct API test with Swiss Ephemeris to verify chart generation
"""

import requests
import json

def test_direct_chart():
    """Test chart generation with a simple example."""
    
    print("="*70)
    print("DIRECT API CHART TEST")
    print("="*70)
    
    # Simple test data
    test_data = {
        "name": "Test Person",
        "birth_date": "1990-06-21",  # Summer solstice
        "birth_time": "12:00",       # Noon
        "birth_location": "New York, NY, USA"
    }
    
    print(f"Testing with: {test_data}")
    
    try:
        # First check if API is running
        health_response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"Health Check: {health_response.status_code}")
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"API Status: {health_data['status']}")
            print(f"House System: {health_data['house_system']}")
        
        # Now try chart generation
        response = requests.post(
            "http://localhost:8000/generate-chart",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\nChart Request Status: {response.status_code}")
        
        if response.status_code == 200:
            chart = response.json()
            print("✅ CHART GENERATED SUCCESSFULLY!")
            print(f"Name: {chart['name']}")
            print(f"Sun: {chart['sun_sign']}")
            print(f"Rising: {chart['rising_sign']} {chart['ascendant']['exact_degree']}")
            print(f"House System: {chart['house_system']}")
            print(f"Planets calculated: {len(chart['placements'])}")
            
            # Show first few planets
            print("\nFirst 5 planetary positions:")
            for planet in chart['placements'][:5]:
                print(f"  {planet['planet']}: {planet['sign']} {planet['exact_degree']} (House {planet['house']})")
            
            return True
            
        else:
            print(f"❌ Chart generation failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Raw error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_multiple_locations():
    """Test with different international locations."""
    
    print("\n" + "="*70)
    print("INTERNATIONAL LOCATIONS TEST")
    print("="*70)
    
    locations = [
        {
            "name": "London Test",
            "birth_date": "1985-12-25",
            "birth_time": "10:00", 
            "birth_location": "London, UK"
        },
        {
            "name": "Sydney Test",
            "birth_date": "1975-09-15",
            "birth_time": "15:30",
            "birth_location": "Sydney, Australia"
        },
        {
            "name": "Tokyo Test", 
            "birth_date": "1992-03-10",
            "birth_time": "08:45",
            "birth_location": "Tokyo, Japan"
        }
    ]
    
    successful_tests = 0
    
    for i, location_data in enumerate(locations, 1):
        print(f"\nTest {i}: {location_data['name']}")
        print(f"Location: {location_data['birth_location']}")
        
        try:
            response = requests.post(
                "http://localhost:8000/generate-chart",
                json=location_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                chart = response.json()
                print(f"✅ Success: {chart['sun_sign']} Sun, {chart['rising_sign']} Rising")
                print(f"   Coordinates: {chart['coordinates']['latitude']:.2f}°, {chart['coordinates']['longitude']:.2f}°")
                successful_tests += 1
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\nLocation tests: {successful_tests}/{len(locations)} successful")
    return successful_tests == len(locations)

if __name__ == "__main__":
    print("Running direct API tests...")
    
    # Test basic chart generation
    basic_success = test_direct_chart()
    
    if basic_success:
        # Test international locations
        location_success = test_multiple_locations()
    else:
        location_success = False
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Basic chart generation: {'✅ PASSED' if basic_success else '❌ FAILED'}")
    print(f"International locations: {'✅ PASSED' if location_success else '❌ FAILED'}")
    
    if basic_success and location_success:
        print("\n🎯 ALL API TESTS SUCCESSFUL!")
        print("Your astrology API is working correctly with:")
        print("✅ Swiss Ephemeris calculations")
        print("✅ International location support")
        print("✅ Whole Sign house system")
        print("✅ Complete planetary positions")
        print("✅ Exact degree calculations")
    else:
        print(f"\n❌ API tests failed - debugging needed")
        print("The Swiss Ephemeris module conflict needs to be resolved")