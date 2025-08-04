#!/usr/bin/env python3
"""
Debug specific discrepancies in Mia's chart calculations.
Compare API output with expected values to identify issues.
"""

import requests
import json

def debug_mia_chart():
    """Debug Mia's chart against expected values."""
    
    print("DEBUGGING MIA'S CHART DISCREPANCIES")
    print("="*70)
    
    # Expected values from user
    expected = {
        'rising': {'sign': 'Taurus', 'degree': 19},
        'midheaven': {'sign': 'Aquarius', 'degree': 27},
        'sun': {'sign': 'Scorpio', 'degree': 29, 'house': 7},
        'moon': {'sign': 'Pisces', 'degree': 4, 'house': 11},
        'mercury': {'sign': 'Scorpio', 'degree': 14, 'house': 7},
        'mars': {'sign': 'Scorpio', 'degree': 17, 'house': 7},
        'venus': {'sign': 'Sagittarius', 'degree': 3, 'house': 8},
        'north_node': {'sign': 'Sagittarius', 'degree': 10, 'house': 8}
    }
    
    # GPT returned (incorrect)
    gpt_returned = {
        'rising': {'sign': 'Taurus', 'degree': 0},
        'midheaven': {'sign': 'Aquarius', 'degree': 28},
        'sun': {'sign': 'Scorpio', 'degree': 29, 'house': 7},
        'moon': {'sign': 'Pisces', 'degree': 2, 'house': 10},
        'mercury': {'sign': 'Scorpio', 'degree': 21, 'house': 6},
        'mars': {'sign': 'Scorpio', 'degree': 25, 'house': 6},
        'venus': {'sign': 'Sagittarius', 'degree': 0, 'house': 7},
        'north_node': {'sign': 'Sagittarius', 'degree': 8, 'house': 8}
    }
    
    print("ISSUE ANALYSIS:")
    print("-" * 40)
    
    print("1. RISING SIGN DEGREE:")
    print(f"   Expected: Taurus 19°")
    print(f"   GPT got: Taurus 0°")
    print(f"   Issue: 19 degree difference - major calculation error")
    print()
    
    print("2. HOUSE ASSIGNMENTS:")
    print(f"   Moon: Expected 11th house → GPT got 10th house")
    print(f"   Mercury: Expected 7th house → GPT got 6th house") 
    print(f"   Mars: Expected 7th house → GPT got 6th house")
    print(f"   Venus: Expected 8th house → GPT got 7th house")
    print(f"   Issue: All houses are off by 1, suggests rising sign error")
    print()
    
    print("3. PLANETARY DEGREES:")
    print(f"   Moon: Expected 4° → GPT got 2° (2° difference)")
    print(f"   Mercury: Expected 14° → GPT got 21° (7° difference)")
    print(f"   Mars: Expected 17° → GPT got 25° (8° difference)")
    print(f"   Venus: Expected 3° → GPT got 0° (3° difference)")
    print(f"   Issue: Significant degree differences suggest calculation problems")
    print()
    
    # Test our API
    try:
        print("TESTING OUR API:")
        print("-" * 40)
        
        response = requests.post(
            "http://localhost:8000/generate-chart",
            json={
                "name": "Mia",
                "birth_date": "1974-11-22",
                "birth_time": "19:10",
                "birth_location": "Adelaide, Australia"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            chart = response.json()
            
            # Check rising sign
            rising_sign = chart['rising_sign']
            rising_degree = chart['ascendant']['exact_degree']
            print(f"Our API Rising: {rising_sign} {rising_degree}")
            
            # Check midheaven
            mc_sign = chart['midheaven']['sign']
            mc_degree = chart['midheaven']['exact_degree']
            print(f"Our API Midheaven: {mc_sign} {mc_degree}")
            
            # Check planetary positions
            planets_data = {}
            for p in chart['placements']:
                planets_data[p['planet']] = p
            
            print(f"\nOur API Planetary Positions:")
            key_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'North Node']
            
            for planet in key_planets:
                if planet in planets_data:
                    p = planets_data[planet]
                    expected_planet = expected.get(planet.lower().replace(' ', '_'), {})
                    exp_deg = expected_planet.get('degree', '?')
                    exp_house = expected_planet.get('house', '?')
                    
                    print(f"  {planet}: {p['sign']} {p['exact_degree']} (House {p['house']})")
                    print(f"    Expected: {expected_planet.get('sign', '?')} {exp_deg}° (House {exp_house})")
                    print()
            
            return chart
            
        else:
            print(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"API Test Error: {e}")
        return None

def identify_root_cause(api_chart):
    """Identify the root cause of discrepancies."""
    
    print("\nROOT CAUSE ANALYSIS:")
    print("="*70)
    
    if not api_chart:
        print("Cannot analyze - API test failed")
        return
    
    # Check if our API matches expected values
    rising_degree = api_chart['ascendant']['exact_degree']
    
    if "19°" in rising_degree:
        print("✅ Our API has correct Taurus 19° rising")
        print("❌ Issue is in GPT integration or data parsing")
        print()
        print("LIKELY CAUSES:")
        print("1. GPT is parsing degrees incorrectly")
        print("2. API response format confusion")
        print("3. GPT action schema needs updating")
        print("4. Rounding errors in degree display")
        
    else:
        print("❌ Our API also has incorrect rising sign")
        print("🔧 Need to fix backend calculations")
        print()
        print("LIKELY CAUSES:")
        print("1. Timezone calculation still incorrect")
        print("2. Coordinate precision issues")
        print("3. Julian day calculation error")
        print("4. Swiss Ephemeris configuration problem")

if __name__ == "__main__":
    api_result = debug_mia_chart()
    identify_root_cause(api_result)
    
    print("\nNEXT STEPS:")
    print("-" * 30)
    print("1. Verify our API produces correct Taurus 19° rising")
    print("2. If API is correct, debug GPT integration")
    print("3. If API is wrong, fix backend calculations")
    print("4. Update GPT schema if needed")
    print("5. Test with reference astrological software")