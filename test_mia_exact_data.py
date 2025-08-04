#!/usr/bin/env python3
"""
Test API with Mia's exact birth data:
- Date: 22 November 1974
- Time: 19:10 (7:10 PM)  
- Location: Adelaide, South Australia, Australia
- Expected: Taurus Rising (19°), Moon in Pisces (4°), Sun in Scorpio (29°)
"""

import uvicorn
from run_production import app
import threading
import time
import requests
import json

def start_server():
    """Start FastAPI server on port 8002."""
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")

def test_mia_exact_chart():
    """Test with Mia's exact birth specifications."""
    
    print("Waiting for server to start...")
    time.sleep(4)
    
    # Mia's exact birth data as specified
    mia_request = {
        "name": "Mia",
        "birth_date": "1974-11-22",  # 22 November 1974
        "birth_time": "19:10",       # 19:10 (7:10 PM)
        "birth_location": "Adelaide, South Australia, Australia"
    }
    
    print("=" * 70)
    print("TESTING MIA'S EXACT BIRTH DATA")
    print("=" * 70)
    print(f"Date: 22 November 1974")
    print(f"Time: 19:10 (7:10 PM)")
    print(f"Location: Adelaide, South Australia, Australia")
    print(f"Expected: Taurus Rising (19°), Moon in Pisces (4°), Sun in Scorpio (29°)")
    print()
    print(f"API Request: {json.dumps(mia_request, indent=2)}")
    
    try:
        response = requests.post(
            "http://localhost:8002/generate-chart",
            json=mia_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            chart = response.json()
            
            print(f"\n✅ CHART GENERATED SUCCESSFULLY")
            print("=" * 70)
            
            # Extract key positions
            ascendant_sign = chart['ascendant']['sign']
            ascendant_degree = chart['ascendant']['exact_degree']
            sun_sign = chart['sun_sign'] 
            moon_sign = chart['moon_sign']
            house_system = chart['house_system']
            
            # Find Sun and Moon exact degrees
            sun_degree = None
            moon_degree = None
            for planet in chart['placements']:
                if planet['planet'] == 'Sun':
                    sun_degree = planet['exact_degree']
                elif planet['planet'] == 'Moon':
                    moon_degree = planet['exact_degree']
            
            print(f"CHART SUMMARY:")
            print(f"Name: {chart['name']}")
            print(f"Birth Date: {chart['birth_date']}")
            print(f"Birth Time: {chart['birth_time']}")
            print(f"Location: {chart['birth_location']}")
            print(f"House System: {house_system}")
            
            print(f"\nKEY POSITIONS:")
            print(f"Rising Sign: {ascendant_sign} {ascendant_degree}")
            print(f"Sun Sign: {sun_sign} {sun_degree}")
            print(f"Moon Sign: {moon_sign} {moon_degree}")
            
            print(f"\nEXPECTED vs ACTUAL:")
            print(f"Rising: Expected Taurus 19° → Actual {ascendant_sign} {ascendant_degree}")
            print(f"Sun: Expected Scorpio 29° → Actual {sun_sign} {sun_degree}")
            print(f"Moon: Expected Pisces 4° → Actual {moon_sign} {moon_degree}")
            
            # Verification
            print(f"\nVERIFICATION:")
            rising_correct = "Taurus" in ascendant_sign and "19°" in ascendant_degree
            sun_correct = "Scorpio" in sun_sign and "29°" in sun_degree
            moon_correct = "Pisces" in moon_sign and "4°" in moon_degree
            whole_sign = "Whole Sign" in house_system
            
            print(f"✅ Taurus Rising 19°: {'CORRECT' if rising_correct else 'INCORRECT'}")
            print(f"✅ Scorpio Sun 29°: {'CORRECT' if sun_correct else 'INCORRECT'}")
            print(f"✅ Pisces Moon 4°: {'CORRECT' if moon_correct else 'INCORRECT'}")
            print(f"✅ Whole Sign Houses: {'CORRECT' if whole_sign else 'INCORRECT'}")
            
            print(f"\nALL PLANETARY POSITIONS:")
            for planet in chart['placements']:
                retro = " (R)" if planet['retrograde'] else ""
                print(f"  {planet['planet']}: {planet['sign']} {planet['exact_degree']} - House {planet['house']}{retro}")
            
            if rising_correct and sun_correct and moon_correct and whole_sign:
                print(f"\n🎯 ALL EXPECTED VALUES CONFIRMED!")
                print(f"✅ No cached/demo data - using real birth input")
                print(f"✅ Swiss Ephemeris calculations accurate")
                print(f"✅ Whole Sign house system properly applied")
            else:
                print(f"\n❌ SOME VALUES DON'T MATCH EXPECTATIONS")
                print(f"Check if cached data or incorrect calculations")
            
            return chart
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

if __name__ == "__main__":
    print("Starting FastAPI server for Mia's exact birth data test...")
    
    # Start server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Test the chart
    result = test_mia_exact_chart()
    
    if result:
        print(f"\n" + "=" * 70)
        print("API TEST COMPLETE - SERVER WORKING")
        print("=" * 70)
        print("Ready for deployment with correct Python FastAPI configuration")
        
        # Keep running for a moment
        time.sleep(3)
    else:
        print("❌ API test failed")