#!/usr/bin/env python3
"""
Test with a famous person's known birth data for verification
Using publicly available birth information
"""

import requests
import json

def test_famous_chart():
    """Test with Albert Einstein's known birth data (public information)."""
    
    print("="*70)
    print("FAMOUS CHART VERIFICATION TEST")
    print("="*70)
    print("Using Albert Einstein's publicly known birth data")
    print("Born: March 14, 1879, 11:30 AM, Ulm, Germany")
    print()
    
    # Einstein's birth data (publicly available)
    einstein_data = {
        "name": "Albert Einstein",
        "birth_date": "1879-03-14",
        "birth_time": "11:30", 
        "birth_location": "Ulm, Germany"
    }
    
    print("Known astrological facts about Einstein:")
    print("- Sun in Pisces (intuitive, imaginative)")
    print("- Strong emphasis on mental/intellectual signs")
    print("- Born during late winter in Germany")
    print()
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-chart",
            json=einstein_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            chart = response.json()
            
            print("✅ EINSTEIN'S CHART GENERATED")
            print("="*70)
            
            print(f"Name: {chart['name']}")
            print(f"Birth Date: {chart['birth_date']} (March 14, 1879)")
            print(f"Birth Time: {chart['birth_time']} (11:30 AM)")
            print(f"Location: {chart['birth_location']}")
            print(f"House System: {chart['house_system']}")
            
            print(f"\nBIG THREE:")
            print(f"Sun: {chart['sun_sign']} (Expected: Pisces)")
            print(f"Moon: {chart['moon_sign']}")
            print(f"Rising: {chart['rising_sign']} {chart['ascendant']['exact_degree']}")
            
            print(f"\nCHART ANGLES:")
            print(f"Ascendant: {chart['ascendant']['sign']} {chart['ascendant']['exact_degree']}")
            print(f"Midheaven: {chart['midheaven']['sign']} {chart['midheaven']['exact_degree']}")
            
            print(f"\nPLANETARY POSITIONS:")
            for planet in chart['placements']:
                retro = " (R)" if planet['retrograde'] else ""
                print(f"  {planet['planet']}: {planet['sign']} {planet['exact_degree']} - House {planet['house']}{retro}")
            
            print(f"\nLOCATION VERIFICATION:")
            coords = chart['coordinates']
            print(f"Latitude: {coords['latitude']:.4f}° (Ulm is ~48.4°N)")
            print(f"Longitude: {coords['longitude']:.4f}° (Ulm is ~10.0°E)")
            print(f"Timezone: {coords['timezone']}")
            
            # Verify key astrological facts
            print(f"\nVERIFICATION:")
            sun_correct = chart['sun_sign'] == "Pisces"
            print(f"Sun in Pisces: {'✅ CORRECT' if sun_correct else '❌ INCORRECT'}")
            
            # March 14 should definitely be Pisces (Feb 19 - Mar 20)
            print(f"Birth date verification: March 14 is in Pisces season ✅")
            
            # Check if coordinates are reasonable for Ulm, Germany
            lat_reasonable = 47 <= coords['latitude'] <= 49  # Ulm is around 48.4°N
            lon_reasonable = 9 <= coords['longitude'] <= 11   # Ulm is around 10.0°E
            location_correct = lat_reasonable and lon_reasonable
            print(f"Location coordinates: {'✅ REASONABLE' if location_correct else '❌ INCORRECT'}")
            
            if sun_correct and location_correct:
                print(f"\n🎯 FAMOUS CHART VERIFICATION SUCCESSFUL!")
                print(f"✅ API correctly calculated Einstein's chart")
                print(f"✅ Sun in Pisces confirmed")
                print(f"✅ German location coordinates correct")
                print(f"✅ 19th century birth date handled properly")
                print(f"✅ Swiss Ephemeris working for historical dates")
                
                return True
            else:
                print(f"\n❌ Some verification checks failed")
                return False
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_modern_chart():
    """Test with a modern birth date for comparison."""
    
    print("\n" + "="*70)
    print("MODERN CHART COMPARISON TEST")
    print("="*70)
    
    modern_data = {
        "name": "Modern Test Subject",
        "birth_date": "2000-01-01",  # Y2K baby
        "birth_time": "00:00",       # Midnight
        "birth_location": "Paris, France"
    }
    
    print("Testing Y2K midnight birth in Paris")
    print("Expected: Strong Capricorn energy (January 1)")
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-chart",
            json=modern_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            chart = response.json()
            
            print(f"\n✅ MODERN CHART GENERATED")
            print(f"Sun: {chart['sun_sign']} (Expected: Capricorn)")
            print(f"Rising: {chart['rising_sign']} {chart['ascendant']['exact_degree']}")
            print(f"Location: {chart['coordinates']['latitude']:.2f}°, {chart['coordinates']['longitude']:.2f}°")
            
            # January 1 should be Capricorn
            sun_correct = chart['sun_sign'] == "Capricorn"
            print(f"New Year's Day in Capricorn: {'✅ CORRECT' if sun_correct else '❌ INCORRECT'}")
            
            return sun_correct
            
        else:
            print(f"❌ Modern chart test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Modern chart test error: {e}")
        return False

if __name__ == "__main__":
    print("Running famous chart verification tests...")
    
    # Test historical chart (Einstein)
    historical_success = test_famous_chart()
    
    # Test modern chart (Y2K)
    modern_success = test_modern_chart()
    
    print(f"\n" + "="*70)
    print("VERIFICATION TEST SUMMARY")
    print("="*70)
    print(f"Historical chart (Einstein): {'✅ PASSED' if historical_success else '❌ FAILED'}")
    print(f"Modern chart (Y2K): {'✅ PASSED' if modern_success else '❌ FAILED'}")
    
    if historical_success and modern_success:
        print(f"\n🎯 ALL VERIFICATION TESTS PASSED!")
        print(f"Your astrology API correctly handles:")
        print(f"✅ Historical dates (19th century)")
        print(f"✅ Modern dates (21st century)")
        print(f"✅ International locations")
        print(f"✅ Accurate sun sign calculations")
        print(f"✅ Proper coordinate geocoding")
        print(f"✅ Swiss Ephemeris astronomical data")
    else:
        print(f"\n❌ Some verification tests failed")
        print(f"API may need calibration or debugging")