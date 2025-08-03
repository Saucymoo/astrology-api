#!/usr/bin/env python3
"""
Simple test of Swiss Ephemeris for Mia's chart.
"""

import swisseph as swe
from datetime import datetime

def test_mia_simple():
    """Simple test of Swiss Ephemeris calculations."""
    
    print("Testing Swiss Ephemeris for Mia's chart...")
    print(f"Swiss Ephemeris version: {swe.version}")
    
    # Mia's birth: November 22, 1974, 19:10, Adelaide
    year = 1974
    month = 11
    day = 22
    hour = 19 + 10/60.0  # 19:10 = 19.167 hours
    
    # Adelaide coordinates
    latitude = -34.9285
    longitude = 138.6007
    
    print(f"Birth: {year}-{month:02d}-{day:02d} {hour:.2f} hours")
    print(f"Location: {latitude}°, {longitude}°")
    
    # Calculate Julian day
    julian_day = swe.julday(year, month, day, hour, swe.GREG_CAL)
    print(f"Julian day: {julian_day}")
    
    # Calculate Sun position
    sun_pos, _ = swe.calc_ut(julian_day, swe.SUN, swe.FLG_SWIEPH)
    sun_longitude = sun_pos[0]
    sun_sign_num = int(sun_longitude // 30) + 1
    sun_degree = sun_longitude % 30
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sun_sign = signs[sun_sign_num - 1]
    
    print(f"Sun: {sun_sign} {sun_degree:.2f}°")
    
    # Calculate Ascendant
    houses_data, ascmc = swe.houses(julian_day, latitude, longitude, b'P')
    asc_longitude = ascmc[0]
    asc_sign_num = int(asc_longitude // 30) + 1
    asc_degree = asc_longitude % 30
    asc_sign = signs[asc_sign_num - 1]
    
    print(f"Ascendant: {asc_sign} {asc_degree:.2f}°")
    
    # Check if results match expectations
    print(f"\nVerification:")
    if sun_sign == "Scorpio" and 28 <= sun_degree <= 30:
        print("✓ Sun position correct: Late Scorpio for Nov 22, 1974")
    else:
        print(f"⚠ Sun position: {sun_sign} {sun_degree:.2f}° (Expected ~29° Scorpio)")
        
    if asc_sign == "Taurus" and 15 <= asc_degree <= 25:
        print("✓ Ascendant correct: Taurus Rising in expected range")
    else:
        print(f"⚠ Ascendant: {asc_sign} {asc_degree:.2f}° (Expected ~19° Taurus)")

if __name__ == "__main__":
    test_mia_simple()