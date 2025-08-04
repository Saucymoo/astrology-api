#!/usr/bin/env python3
"""
Debug Saturn retrograde calculation specifically for Mia's chart.
"""

import requests
import json
import swisseph as swe
from datetime import datetime
from zoneinfo import ZoneInfo

def debug_saturn_calculation():
    """Debug Saturn retrograde calculation at multiple levels."""
    
    print("DEBUGGING SATURN RETROGRADE CALCULATION")
    print("="*50)
    
    # 1. Direct Swiss Ephemeris calculation
    print("1. DIRECT SWISS EPHEMERIS TEST:")
    print("-" * 30)
    
    # Calculate Julian Day for November 22, 1974, 19:10 Adelaide
    # Adelaide was UTC+10:30 in November 1974 (daylight saving)
    dt_local = datetime(1974, 11, 22, 19, 10)
    adelaide_tz = ZoneInfo('Australia/Adelaide')
    dt_local_tz = dt_local.replace(tzinfo=adelaide_tz)
    dt_utc = dt_local_tz.utctimetuple()
    
    jd = swe.julday(dt_utc.tm_year, dt_utc.tm_mon, dt_utc.tm_mday, 
                    dt_utc.tm_hour + dt_utc.tm_min/60.0)
    
    print(f"Julian Day: {jd}")
    
    # Calculate Saturn directly
    result = swe.calc_ut(jd, swe.SATURN)
    longitude = result[0][0]
    speed = result[0][3]
    
    print(f"Saturn longitude: {longitude:.6f}°")
    print(f"Saturn speed: {speed:.6f}°/day")
    print(f"Saturn retrograde: {speed < 0}")
    
    # 2. Test our API
    print(f"\n2. API RESPONSE TEST:")
    print("-" * 30)
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-chart",
            json={
                "name": "Mia Mitchell",
                "birth_date": "1974-11-22",
                "birth_time": "19:10",
                "birth_location": "Adelaide, South Australia, Australia"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            chart = response.json()
            
            # Find Saturn
            saturn_data = None
            for planet in chart['placements']:
                if planet['planet'] == 'Saturn':
                    saturn_data = planet
                    break
            
            if saturn_data:
                print(f"API Saturn: {saturn_data['sign']} {saturn_data['exact_degree']}")
                print(f"API Saturn retrograde: {saturn_data.get('retrograde', 'Missing!')}")
                print(f"API Saturn house: {saturn_data.get('house', 'Missing!')}")
                
                # Compare calculations
                api_retro = saturn_data.get('retrograde', False)
                direct_retro = speed < 0
                
                print(f"\nCOMPARISON:")
                print(f"Direct calculation: {direct_retro}")
                print(f"API calculation: {api_retro}")
                print(f"Match: {api_retro == direct_retro}")
                
                if api_retro != direct_retro:
                    print(f"\n❌ MISMATCH DETECTED!")
                    print(f"The API is not correctly calculating Saturn's retrograde status")
                else:
                    print(f"\n✅ CALCULATIONS MATCH!")
            else:
                print("❌ Saturn not found in API response!")
                
        else:
            print(f"API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"API Test Error: {e}")

if __name__ == "__main__":
    debug_saturn_calculation()