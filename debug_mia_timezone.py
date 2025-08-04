#!/usr/bin/env python3
"""
Debug Mia's timezone and birth time to get correct Taurus 19° rising
"""

try:
    import swisseph as swe
except ImportError:
    swe = None

import requests
from datetime import datetime

def test_different_timezone_offsets():
    """Test different timezone interpretations for Adelaide in November 1974."""
    
    print("DEBUGGING MIA'S BIRTH TIME FOR CORRECT TAURUS RISING")
    print("="*70)
    print("Expected: Taurus 19° Rising, Aquarius 27° Midheaven")
    print("Current: Gemini 1° Rising, Pisces 13° Midheaven")
    print()
    
    if not swe:
        print("Swiss Ephemeris not available for direct calculation")
        return
    
    # Mia's birth data
    year, month, day = 1974, 11, 22
    hour, minute = 19, 10  # 7:10 PM
    lat, lon = -34.9285, 138.6007  # Adelaide
    
    print(f"Birth: {day} Nov {year}, {hour}:{minute:02d} ({hour}:{minute:02d} PM)")
    print(f"Location: Adelaide ({lat:.4f}°, {lon:.4f}°)")
    print()
    
    # Test different timezone interpretations
    timezone_tests = [
        {"name": "Standard Time (UTC+9:30)", "offset": 9.5, "description": "No daylight saving"},
        {"name": "Daylight Saving (UTC+10:30)", "offset": 10.5, "description": "With daylight saving"},
        {"name": "Standard Time (UTC+9:00)", "offset": 9.0, "description": "Without 30min offset"},
        {"name": "Local Mean Time", "offset": lon/15, "description": "Based on longitude"},
        {"name": "Current API Calculation", "offset": 9.5, "description": "What API is using"}
    ]
    
    results = []
    
    for test in timezone_tests:
        print(f"Testing: {test['name']} ({test['description']})")
        
        try:
            # Convert to UTC
            decimal_local = hour + minute/60.0
            decimal_utc = decimal_local - test['offset']
            
            utc_day = day
            if decimal_utc < 0:
                decimal_utc += 24
                utc_day -= 1
            elif decimal_utc >= 24:
                decimal_utc -= 24
                utc_day += 1
            
            # Calculate Julian Day
            jd = swe.julday(year, month, utc_day, decimal_utc)
            
            # Calculate houses using Placidus for angles
            houses, ascmc = swe.houses(jd, lat, lon, b'P')
            
            asc_deg = ascmc[0]
            mc_deg = ascmc[1]
            
            # Convert to sign format
            def deg_to_sign(deg):
                signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
                sign_idx = int(deg // 30)
                sign_deg = deg % 30
                return f"{signs[sign_idx]} {sign_deg:.1f}°"
            
            asc_result = deg_to_sign(asc_deg)
            mc_result = deg_to_sign(mc_deg)
            
            # Check if closer to expected
            asc_taurus = "Taurus" in asc_result
            mc_aquarius = "Aquarius" in mc_result
            
            print(f"  Ascendant: {asc_result} {'✓' if asc_taurus else '✗'}")
            print(f"  Midheaven: {mc_result} {'✓' if mc_aquarius else '✗'}")
            print(f"  Match: {'CLOSER' if asc_taurus or mc_aquarius else 'NO MATCH'}")
            
            results.append({
                'test': test['name'],
                'offset': test['offset'],
                'asc': asc_result,
                'mc': mc_result,
                'asc_match': asc_taurus,
                'mc_match': mc_aquarius,
                'jd': jd
            })
            
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    # Find best match
    best_results = [r for r in results if r.get('asc_match') or r.get('mc_match')]
    
    if best_results:
        print("BEST MATCHES:")
        for result in best_results:
            print(f"  {result['test']}: ASC {result['asc']}, MC {result['mc']}")
    else:
        print("No exact matches found. May need to check:")
        print("- Birth time accuracy (exact minute)")
        print("- Historical timezone rules for Adelaide 1974")
        print("- Coordinate precision")
    
    return results

def test_time_variations():
    """Test slight time variations around 19:10."""
    
    print("\n" + "="*70)
    print("TIME VARIATION TEST")
    print("="*70)
    
    if not swe:
        return
    
    base_hour, base_minute = 19, 10
    lat, lon = -34.9285, 138.6007
    year, month, day = 1974, 11, 22
    
    # Test times around 19:10
    time_tests = [
        (19, 5), (19, 8), (19, 10), (19, 12), (19, 15),
        (18, 55), (18, 58), (19, 0), (19, 20), (19, 25)
    ]
    
    print("Testing times around 7:10 PM for Taurus rising:")
    
    for test_hour, test_minute in time_tests:
        try:
            decimal_local = test_hour + test_minute/60.0
            decimal_utc = decimal_local - 9.5  # Adelaide standard offset
            
            utc_day = day
            if decimal_utc < 0:
                decimal_utc += 24
                utc_day -= 1
                
            jd = swe.julday(year, month, utc_day, decimal_utc)
            houses, ascmc = swe.houses(jd, lat, lon, b'P')
            
            asc_deg = ascmc[0] % 360
            sign_idx = int(asc_deg // 30)
            sign_deg = asc_deg % 30
            
            signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
            
            result = f"{signs[sign_idx]} {sign_deg:.1f}°"
            taurus_match = "Taurus" in result and 18 <= sign_deg <= 20
            
            print(f"  {test_hour:02d}:{test_minute:02d} → {result} {'★ MATCH' if taurus_match else ''}")
            
        except Exception as e:
            print(f"  {test_hour:02d}:{test_minute:02d} → Error: {e}")

def check_current_api():
    """Check what the current API is returning."""
    
    print("\n" + "="*70)
    print("CURRENT API CHECK")
    print("="*70)
    
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
            
            print("Current API Results:")
            print(f"  Ascendant: {chart['ascendant']['sign']} {chart['ascendant']['exact_degree']}")
            print(f"  Midheaven: {chart['midheaven']['sign']} {chart['midheaven']['exact_degree']}")
            print(f"  Expected: Taurus 19°, Aquarius 27°")
            print()
            print("Discrepancy Analysis:")
            print("- Current shows Gemini rising (next sign after Taurus)")
            print("- Suggests time may be ~1-2 hours too late")
            print("- Or timezone offset needs adjustment")
            
        else:
            print(f"API Error: {response.status_code}")
            
    except Exception as e:
        print(f"API test failed: {e}")

if __name__ == "__main__":
    # Run all debugging tests
    timezone_results = test_different_timezone_offsets()
    test_time_variations()
    check_current_api()
    
    print(f"\n" + "="*70)
    print("DEBUGGING SUMMARY")
    print("="*70)
    print("Expected: Taurus 19° Rising, Aquarius 27° Midheaven")
    print("Current:  Gemini 1° Rising, Pisces 13° Midheaven")
    print()
    print("Next steps:")
    print("1. Check historical Adelaide timezone rules for Nov 1974")
    print("2. Verify exact birth time (may need adjustment)")
    print("3. Test different coordinate precision")
    print("4. Consider local mean time vs standard time")