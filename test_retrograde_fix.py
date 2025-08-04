#!/usr/bin/env python3
"""
Test the retrograde calculation fix for Mia's chart.
"""

import requests
import json

def test_retrograde_fix():
    """Test that Saturn and Chiron show as retrograde."""
    
    print("TESTING RETROGRADE FIX FOR MIA'S CHART")
    print("="*50)
    
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
            
            # Find retrograde planets
            retrograde_planets = []
            all_planets = {}
            
            for planet in chart['placements']:
                all_planets[planet['planet']] = planet
                if planet.get('retrograde', False):
                    retrograde_planets.append(planet['planet'])
            
            print("RETROGRADE STATUS CHECK:")
            print("-" * 30)
            
            # Check specific planets
            saturn = all_planets.get('Saturn', {})
            chiron = all_planets.get('Chiron', {})
            
            print(f"Saturn: {saturn.get('sign', 'N/A')} {saturn.get('exact_degree', 'N/A')} - Retrograde: {saturn.get('retrograde', False)}")
            print(f"Chiron: {chiron.get('sign', 'N/A')} {chiron.get('exact_degree', 'N/A')} - Retrograde: {chiron.get('retrograde', False)}")
            
            print(f"\nAll retrograde planets: {retrograde_planets}")
            
            # Verify expected results
            saturn_retro = saturn.get('retrograde', False)
            chiron_retro = chiron.get('retrograde', False)
            
            print(f"\nRESULTS:")
            print(f"✅ Saturn retrograde: {saturn_retro} (Expected: True)")
            print(f"✅ Chiron retrograde: {chiron_retro} (Expected: True)")
            
            if saturn_retro and chiron_retro:
                print(f"\n🎯 SUCCESS: Both Saturn and Chiron correctly show as retrograde!")
                return True
            else:
                print(f"\n❌ ISSUE: Retrograde status not correct")
                return False
            
        else:
            print(f"API Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Test Error: {e}")
        return False

if __name__ == "__main__":
    test_retrograde_fix()