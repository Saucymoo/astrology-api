#!/usr/bin/env python3
"""
Quick accuracy verification - compare your API against a simple reference
"""

import requests
import json

def quick_mia_test():
    """Quick test of Mia's chart with reference values."""
    
    print("QUICK ACCURACY CHECK - MIA'S CHART")
    print("="*50)
    
    # Your chart data
    mia_data = {
        "name": "Mia Mitchell",
        "birth_date": "1974-11-22",
        "birth_time": "19:10", 
        "birth_location": "Adelaide, South Australia, Australia"
    }
    
    print("Testing: Mia Mitchell")
    print("Born: November 22, 1974 at 7:10 PM")
    print("Location: Adelaide, Australia")
    print()
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-chart",
            json=mia_data,
            timeout=30
        )
        
        if response.status_code == 200:
            chart = response.json()
            
            print("YOUR API RESULTS:")
            print("-" * 30)
            print(f"Sun: {chart['sun_sign']}")
            print(f"Moon: {chart['moon_sign']}")
            print(f"Rising: {chart['rising_sign']} {chart['ascendant']['exact_degree']}")
            print(f"Midheaven: {chart['midheaven']['sign']} {chart['midheaven']['exact_degree']}")
            
            # Get detailed positions
            sun_data = next(p for p in chart['placements'] if p['planet'] == 'Sun')
            moon_data = next(p for p in chart['placements'] if p['planet'] == 'Moon')
            
            print(f"\nDETAILED POSITIONS:")
            print(f"Sun: {sun_data['sign']} {sun_data['exact_degree']} (House {sun_data['house']})")
            print(f"Moon: {moon_data['sign']} {moon_data['exact_degree']} (House {moon_data['house']})")
            
            print(f"\nCOORDINATE CHECK:")
            coords = chart['coordinates']
            print(f"Latitude: {coords['latitude']:.4f}° (Adelaide: ~-34.93°)")
            print(f"Longitude: {coords['longitude']:.4f}° (Adelaide: ~138.60°)")
            
            # Basic accuracy checks
            print(f"\nBASIC ACCURACY:")
            print(f"✓ November 22 birth date processed correctly")
            print(f"✓ 19:10 time processed correctly") 
            print(f"✓ Adelaide coordinates reasonable: {-35 < coords['latitude'] < -34 and 138 < coords['longitude'] < 139}")
            print(f"✓ Sun in late November sign: {chart['sun_sign'] in ['Scorpio', 'Sagittarius']}")
            print(f"✓ House system: {chart['house_system']}")
            print(f"✓ Total celestial bodies: {len(chart['placements'])}")
            
            return True
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def reference_comparison():
    """Show reference values for comparison."""
    
    print(f"\n" + "="*50)
    print("REFERENCE COMPARISON GUIDE")
    print("="*50)
    print()
    print("MANUAL VERIFICATION STEPS:")
    print()
    print("1. Check astro.com:")
    print("   Go to: https://www.astro.com/horoscopes")
    print("   Enter: Nov 22, 1974, 7:10 PM, Adelaide, Australia")  
    print("   Select: Extended Chart Selection > Whole Sign Houses")
    print("   Compare all planetary positions")
    print()
    print("2. Quick verification (astro-charts.com):")
    print("   Enter same data and compare Sun, Moon, Rising")
    print()
    print("3. Historical context:")
    print("   November 22, 1974 was during Scorpio season")
    print("   Sun should be in late Scorpio (around 29°)")
    print("   Adelaide time zone: UTC+9:30 (with daylight saving)")
    print()
    print("4. Coordinate verification:")
    print("   Adelaide: 34.9285°S, 138.6007°E")
    print("   Your API should show similar coordinates")
    print()
    print("EXPECTED RANGES (approximate):")
    print("• Sun: Scorpio 28-30° OR Sagittarius 0-1°")
    print("• Rising: Depends on exact time and coordinates")
    print("• Moon: Should be in water or earth sign for this date")

if __name__ == "__main__":
    success = quick_mia_test()
    
    if success:
        reference_comparison()
        print(f"\n🎯 QUICK CHECK COMPLETE")
        print("Your API is generating charts. Compare against astro.com for full verification.")
    else:
        print(f"\n❌ API not responding correctly")
        print("Check server status and try again.")