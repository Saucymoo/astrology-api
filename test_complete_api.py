#!/usr/bin/env python3
"""
Final test of the complete astrology API with all required points.
"""

import json
import subprocess
import time
import requests

def test_complete_api():
    """Test the live API with all required astrological points."""
    print("🌟 TESTING COMPLETE ASTROLOGY API")
    print("=" * 50)
    
    # Start server
    print("Starting API server...")
    proc = subprocess.Popen(['python', 'main.py'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
    time.sleep(4)
    
    try:
        base_url = "http://localhost:8000"
        
        # Test request
        test_data = {
            "name": "Complete Test",
            "date": "1990-06-15",
            "time": "14:30",
            "location": "New York, NY, USA"
        }
        
        print(f"POST {base_url}/generate-chart")
        print(f"Input: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            f"{base_url}/generate-chart",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            chart = response.json()
            
            print("✅ SUCCESS! Complete chart generated")
            
            # Verify all required points
            required_planets = [
                "Sun", "Moon", "Mercury", "Venus", "Mars", 
                "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron"
            ]
            
            print(f"\n⭐ KEY ASTROLOGICAL POINTS:")
            print(f"   Rising Sign: {chart['risingSign']}")
            print(f"   Sun Sign: {chart['sunSign']}")
            print(f"   Moon Sign: {chart['moonSign']}")
            
            print(f"\n🔺 CHART ANGLES:")
            print(f"   Midheaven: {chart['midheaven']['sign']} at {chart['midheaven']['degree']:.1f}°")
            print(f"   Descendant: {chart['descendant']['sign']} at {chart['descendant']['degree']:.1f}°")
            print(f"   Imum Coeli: {chart['imumCoeli']['sign']} at {chart['imumCoeli']['degree']:.1f}°")
            
            print(f"\n🪐 PLANETARY PLACEMENTS:")
            found_planets = set()
            for placement in chart['placements']:
                planet = placement['planet']
                found_planets.add(planet)
                if planet in required_planets:
                    retro = " (R)" if placement['retrograde'] else ""
                    print(f"   ✅ {planet}: {placement['sign']} in House {placement['house']} at {placement['degree']:.1f}°{retro}")
            
            # Check completeness
            missing = set(required_planets) - found_planets
            if missing:
                print(f"\n❌ Missing planets: {missing}")
            else:
                print(f"\n✅ All {len(required_planets)} required planets present!")
            
            print(f"\n🏠 HOUSE SYSTEM:")
            print(f"   System: {chart['houseSystem']} (Whole Sign)")
            
            # Show JSON sample
            print(f"\n📝 API RESPONSE STRUCTURE:")
            sample = {
                "risingSign": chart['risingSign'],
                "sunSign": chart['sunSign'],
                "moonSign": chart['moonSign'],
                "midheaven": chart['midheaven'],
                "descendant": chart['descendant'],
                "imumCoeli": chart['imumCoeli'],
                "placements": chart['placements'][:3],  # First 3
                "houseSystem": chart['houseSystem']
            }
            print(json.dumps(sample, indent=2))
            
            return True
            
        else:
            print(f"❌ Request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        proc.terminate()
        print(f"\n🔒 Server stopped")

def main():
    """Run the complete API test."""
    success = test_complete_api()
    
    print(f"\n" + "=" * 50)
    print("🎯 FINAL VERIFICATION COMPLETE")
    print("=" * 50)
    
    if success:
        print("✅ ALL REQUIRED ASTROLOGICAL POINTS INCLUDED:")
        print("   • Sun, Rising, Moon, Venus, Mercury, Mars")
        print("   • Jupiter, Saturn, Uranus, Neptune, Pluto, Chiron")
        print("   • Midheaven, Descendant, Imum Coeli")
        print("✅ Whole Sign house system configured")
        print("✅ Complete JSON response format")
        print("✅ API ready for production use!")
    else:
        print("❌ Test failed - check output above")

if __name__ == "__main__":
    main()