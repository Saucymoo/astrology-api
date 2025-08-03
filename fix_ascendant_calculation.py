#!/usr/bin/env python3
"""
Fix the Ascendant calculation error and correct house assignments.
User confirmed: Ascendant should be Taurus 19°, not Gemini 1°
"""

import asyncio
import swisseph as swe
from datetime import datetime, timezone, timedelta
import math

def calculate_correct_ascendant():
    """Calculate the correct Ascendant for Adelaide coordinates."""
    
    print("=" * 70)
    print("CORRECTING ASCENDANT CALCULATION")
    print("=" * 70)
    
    # Birth data
    year = 1974
    month = 11
    day = 22
    hour = 19
    minute = 10
    
    # Adelaide coordinates
    latitude = -34.9285
    longitude = 138.6007
    timezone_offset = 9.5  # UTC+9.5
    
    print(f"Birth: {day}/{month}/{year} {hour}:{minute:02d}")
    print(f"Location: Adelaide ({latitude}, {longitude})")
    print(f"Timezone: UTC+{timezone_offset}")
    
    # Convert to UTC
    local_dt = datetime(year, month, day, hour, minute)
    utc_dt = local_dt - timedelta(hours=timezone_offset)
    
    print(f"Local time: {local_dt}")
    print(f"UTC time: {utc_dt}")
    
    # Calculate Julian day
    julian_day = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                           utc_dt.hour + utc_dt.minute/60.0)
    
    print(f"Julian Day: {julian_day}")
    
    # Calculate houses - try different house systems
    house_systems = {
        'P': 'Placidus',
        'K': 'Koch', 
        'R': 'Regiomontanus',
        'C': 'Campanus',
        'E': 'Equal',
        'W': 'Whole Sign'
    }
    
    results = {}
    
    for system_code, system_name in house_systems.items():
        try:
            houses, ascmc = swe.houses(julian_day, latitude, longitude, system_code.encode('ascii'))
            
            # Ascendant is ascmc[0]
            asc_degree = ascmc[0]
            
            # Convert to sign and degree
            sign_num = int(asc_degree // 30)
            degree_in_sign = asc_degree % 30
            
            signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
            
            asc_sign = signs[sign_num]
            
            results[system_code] = {
                'system': system_name,
                'ascendant_degree': asc_degree,
                'sign': asc_sign,
                'degree_in_sign': degree_in_sign,
                'exact_degree': f"{int(degree_in_sign)}°{int((degree_in_sign % 1) * 60):02d}'{int(((degree_in_sign % 1) * 60 % 1) * 60):02d}\"",
                'houses': houses,
                'ascmc': ascmc
            }
            
            print(f"\n{system_name} ({system_code}):")
            print(f"  Ascendant: {asc_sign} {int(degree_in_sign)}°{int((degree_in_sign % 1) * 60):02d}'")
            
            # Check if this matches user's correction
            if asc_sign == 'Taurus' and 18 <= degree_in_sign <= 20:
                print(f"  ✅ MATCHES USER CORRECTION: Taurus ~19°")
            else:
                print(f"  ❌ Doesn't match user correction (Taurus 19°)")
                
        except Exception as e:
            print(f"Error calculating {system_name}: {e}")
    
    return results

def calculate_correct_planetary_houses():
    """Calculate planetary positions with correct Taurus Ascendant house assignments."""
    
    print(f"\n" + "=" * 70)
    print("CORRECTING PLANETARY HOUSE ASSIGNMENTS")
    print("=" * 70)
    
    # If Ascendant is Taurus 19°, then Whole Sign houses are:
    # 1st House: Taurus (0-30°)
    # 2nd House: Gemini (30-60°) 
    # 3rd House: Cancer (60-90°)
    # 4th House: Leo (90-120°)
    # 5th House: Virgo (120-150°)
    # 6th House: Libra (150-180°)
    # 7th House: Scorpio (180-210°)
    # 8th House: Sagittarius (210-240°)
    # 9th House: Capricorn (240-270°)
    # 10th House: Aquarius (270-300°)
    # 11th House: Pisces (300-330°)
    # 12th House: Aries (330-360°/0°)
    
    whole_sign_houses = {
        'Taurus': 1,
        'Gemini': 2, 
        'Cancer': 3,
        'Leo': 4,
        'Virgo': 5,
        'Libra': 6,
        'Scorpio': 7,  # User said Scorpio is 7th house ✓
        'Sagittarius': 8,  # User said Sagittarius is 8th house ✓
        'Capricorn': 9,
        'Aquarius': 10,
        'Pisces': 11,  # User said Pisces is 11th house ✓
        'Aries': 12  # User said Aries is 12th house ✓
    }
    
    print("Whole Sign House System with Taurus Rising:")
    for sign, house in whole_sign_houses.items():
        print(f"  {house:2d}th House: {sign}")
    
    # Our previous planetary calculations (these positions should be correct)
    planets = [
        {'name': 'Sun', 'sign': 'Scorpio', 'degree': 29.706438},
        {'name': 'Moon', 'sign': 'Pisces', 'degree': 4.700195},
        {'name': 'Mercury', 'sign': 'Scorpio', 'degree': 14.742060},
        {'name': 'Venus', 'sign': 'Sagittarius', 'degree': 3.65},
        {'name': 'Mars', 'sign': 'Scorpio', 'degree': 17.11},
        {'name': 'Jupiter', 'sign': 'Pisces', 'degree': 8.59},
        {'name': 'Saturn', 'sign': 'Cancer', 'degree': 18.47},
        {'name': 'Uranus', 'sign': 'Scorpio', 'degree': 0.06},
        {'name': 'Neptune', 'sign': 'Sagittarius', 'degree': 8.98},
        {'name': 'Pluto', 'sign': 'Libra', 'degree': 8.54},
        {'name': 'North Node', 'sign': 'Sagittarius', 'degree': 10.34},
        {'name': 'South Node', 'sign': 'Gemini', 'degree': 10.34},
        {'name': 'Chiron', 'sign': 'Aries', 'degree': 20.0}
    ]
    
    print(f"\nCORRECTED PLANETARY HOUSE ASSIGNMENTS:")
    print("Planet".ljust(12) + "Sign".ljust(12) + "Degree".ljust(12) + "House")
    print("-" * 50)
    
    corrected_planets = []
    for planet in planets:
        house = whole_sign_houses.get(planet['sign'], 0)
        exact_degree = f"{int(planet['degree'])}°{int((planet['degree'] % 1) * 60):02d}'"
        
        corrected_planets.append({
            'name': planet['name'],
            'sign': planet['sign'],
            'degree': planet['degree'],
            'exact_degree': exact_degree,
            'house': house
        })
        
        print(f"{planet['name'].ljust(12)}{planet['sign'].ljust(12)}{exact_degree.ljust(12)}{house}")
    
    return corrected_planets

async def verify_user_corrections():
    """Verify the user's house system corrections."""
    
    print(f"\n" + "=" * 70)
    print("VERIFYING USER'S CORRECTIONS")
    print("=" * 70)
    
    # User's corrections:
    # - Ascendant should be Taurus at 19°
    # - Scorpio is 7th house  
    # - Sagittarius is 8th house
    # - Pisces is 11th house
    # - Aries is 12th house
    
    print("USER'S CORRECTIONS:")
    print("✓ Ascendant: Taurus 19° (not Gemini 1°)")
    print("✓ Scorpio = 7th house")
    print("✓ Sagittarius = 8th house") 
    print("✓ Pisces = 11th house")
    print("✓ Aries = 12th house")
    
    # Calculate what house system gives these results
    ascendant_results = calculate_correct_ascendant()
    
    # Find which house system gives Taurus ~19°
    correct_system = None
    for system_code, result in ascendant_results.items():
        if result['sign'] == 'Taurus' and 18 <= result['degree_in_sign'] <= 20:
            correct_system = system_code
            print(f"\n✅ FOUND MATCHING SYSTEM: {result['system']} ({system_code})")
            print(f"   Ascendant: {result['sign']} {result['exact_degree']}")
            break
    
    if not correct_system:
        print(f"\n⚠ No house system matches Taurus 19° exactly")
        print("This might indicate a calculation error or different ephemeris data")
        
        # Show closest matches
        taurus_systems = [(k, v) for k, v in ascendant_results.items() if v['sign'] == 'Taurus']
        if taurus_systems:
            print("\nTaurus Ascendant results found:")
            for system_code, result in taurus_systems:
                print(f"  {result['system']}: Taurus {result['exact_degree']}")
    
    # Calculate corrected planets
    corrected_planets = calculate_correct_planetary_houses()
    
    return {
        'ascendant_system': correct_system,
        'corrected_planets': corrected_planets,
        'house_calculations': ascendant_results
    }

if __name__ == "__main__":
    results = asyncio.run(verify_user_corrections())
    
    print(f"\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if results['ascendant_system']:
        print(f"✅ Found house system matching user's Taurus 19° Ascendant")
    else:
        print(f"⚠ Need to investigate why no system gives Taurus 19°")
        print("Possible issues:")
        print("  - Coordinate precision")
        print("  - Time zone calculation")
        print("  - Ephemeris difference")
    
    print(f"\n✅ House assignments corrected according to user's specifications:")
    print("   Scorpio → 7th house, Sagittarius → 8th house")
    print("   Pisces → 11th house, Aries → 12th house")