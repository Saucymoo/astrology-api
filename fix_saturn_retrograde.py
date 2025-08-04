#!/usr/bin/env python3
"""
Fix Saturn retrograde calculation by identifying the exact discrepancy.
"""

import swisseph as swe
from datetime import datetime
from zoneinfo import ZoneInfo

def compare_julian_day_calculations():
    """Compare different Julian Day calculation methods."""
    
    print("JULIAN DAY CALCULATION COMPARISON")
    print("="*50)
    
    # Method 1: Direct calculation (known correct)
    dt_local = datetime(1974, 11, 22, 19, 10)
    adelaide_tz = ZoneInfo('Australia/Adelaide')
    dt_local_tz = dt_local.replace(tzinfo=adelaide_tz)
    dt_utc = dt_local_tz.utctimetuple()
    
    jd_direct = swe.julday(dt_utc.tm_year, dt_utc.tm_mon, dt_utc.tm_mday, 
                          dt_utc.tm_hour + dt_utc.tm_min/60.0)
    
    print(f"Direct calculation JD: {jd_direct}")
    
    # Method 2: Simulate our API's timezone handler
    # The API uses Adelaide UTC+9 offset (should be UTC+10:30 for November 1974)
    
    # Simulate what the API might be doing (potential issue)
    hour = 19
    minute = 10
    decimal_local_time = hour + minute / 60.0
    
    # If API uses UTC+9 instead of UTC+10:30 DST
    decimal_utc_time_wrong = decimal_local_time - 9  # Wrong offset
    jd_wrong = swe.julday(1974, 11, 22, decimal_utc_time_wrong)
    
    # Correct DST offset for November 1974
    decimal_utc_time_correct = decimal_local_time - 10.5  # Correct offset
    jd_correct = swe.julday(1974, 11, 22, decimal_utc_time_correct)
    
    print(f"API wrong offset JD: {jd_wrong}")
    print(f"API correct offset JD: {jd_correct}")
    
    # Test Saturn at each JD
    print(f"\nSATURN SPEED AT DIFFERENT JULIAN DAYS:")
    print("-" * 40)
    
    for name, jd in [("Direct", jd_direct), ("Wrong offset", jd_wrong), ("Correct offset", jd_correct)]:
        result = swe.calc_ut(jd, swe.SATURN)
        speed = result[0][3]
        retrograde = speed < 0
        print(f"{name:15}: JD={jd:.6f}, Speed={speed:.6f}, Retro={retrograde}")
    
    # Find which matches our API
    print(f"\nLIKELY ISSUE:")
    if abs(jd_wrong - jd_direct) < abs(jd_correct - jd_direct):
        print("API is probably using the wrong timezone offset")
    else:
        print("Issue may be elsewhere in the calculation")

def fix_retrograde_in_api():
    """Test a potential fix by ensuring correct speed calculation."""
    
    print(f"\nTESTING POTENTIAL FIX")
    print("="*50)
    
    # Test with correct Adelaide timezone
    dt = datetime(1974, 11, 22, 19, 10)
    adelaide_tz = ZoneInfo('Australia/Adelaide')
    dt_tz = dt.replace(tzinfo=adelaide_tz)
    
    # Convert to UTC properly
    dt_utc = dt_tz.utctimetuple()
    jd = swe.julday(dt_utc.tm_year, dt_utc.tm_mon, dt_utc.tm_mday, 
                    dt_utc.tm_hour + dt_utc.tm_min/60.0)
    
    print(f"Fixed Julian Day: {jd}")
    
    # Test all planets for retrograde status
    planets = {
        'Saturn': swe.SATURN,
        'Jupiter': swe.JUPITER,
        'Mars': swe.MARS,
        'Venus': swe.VENUS,
        'Mercury': swe.MERCURY
    }
    
    print(f"\nRETROGRADE STATUS WITH FIXED CALCULATION:")
    print("-" * 40)
    
    for name, planet_id in planets.items():
        result = swe.calc_ut(jd, planet_id)
        speed = result[0][3]
        retrograde = speed < 0
        print(f"{name:8}: Speed={speed:8.4f}°/day, Retrograde={retrograde}")

if __name__ == "__main__":
    compare_julian_day_calculations()
    fix_retrograde_in_api()