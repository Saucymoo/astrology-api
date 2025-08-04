#!/usr/bin/env python3
"""
Simple chart test to verify basic functionality
"""

import requests
import json

def simple_chart_test():
    """Run a simple chart test with basic data."""
    
    print("SIMPLE CHART TEST")
    print("="*50)
    
    # Test with your birth data (Mia)
    test_data = {
        "name": "Mia",
        "birth_date": "1974-11-22",
        "birth_time": "19:10",
        "birth_location": "Adelaide, South Australia, Australia"
    }
    
    print(f"Testing: {test_data['name']}")
    print(f"Born: {test_data['birth_date']} at {test_data['birth_time']}")
    print(f"Location: {test_data['birth_location']}")
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-chart",
            json=test_data,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            chart = response.json()
            
            print("✅ SUCCESS! Chart generated")
            print("-" * 50)
            print(f"Name: {chart['name']}")
            print(f"Sun: {chart['sun_sign']}")
            print(f"Moon: {chart['moon_sign']}")
            print(f"Rising: {chart['rising_sign']} {chart['ascendant']['exact_degree']}")
            print(f"House System: {chart['house_system']}")
            
            print(f"\nPlanetary Count: {len(chart['placements'])}")
            print("First 3 planets:")
            for planet in chart['placements'][:3]:
                retro = " (R)" if planet['retrograde'] else ""
                print(f"  {planet['planet']}: {planet['sign']} {planet['exact_degree']}{retro}")
            
            return True
            
        else:
            print("❌ FAILED")
            try:
                error = response.json()
                print(f"Error: {error['detail']}")
            except:
                print(f"Raw error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    success = simple_chart_test()
    
    if success:
        print("\n🎯 Chart generation is working!")
        print("Ready for GPT integration")
    else:
        print("\n❌ Chart generation needs debugging")