#!/usr/bin/env python3
"""
Generate Mia's correct natal chart using DD/MM/YYYY format.
"""

import asyncio
import json
import subprocess
import time
import sys
import requests

async def generate_mia_correct_chart():
    """Generate Mia's natal chart with correct date format."""
    
    print("GENERATING MIA'S CORRECT NATAL CHART")
    print("=" * 60)
    
    # Start the server
    proc = subprocess.Popen([sys.executable, 'main.py'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Mia's birth data with correct Australian format
        birth_data = {
            'name': 'Mia',
            'date': '22/11/1974',  # DD/MM/YYYY - November 22, 1974
            'time': '19:10',
            'location': 'Adelaide, South Australia, Australia'
        }
        
        print(f"Birth Information (Corrected):")
        print(f"  Name: {birth_data['name']}")
        print(f"  Date: {birth_data['date']} (DD/MM/YYYY format)")
        print(f"  Interpreted as: November 22, 1974")
        print(f"  Time: {birth_data['time']}")
        print(f"  Location: {birth_data['location']}")
        
        print("\nGenerating chart with Whole Sign houses...")
        print("Expected: Sun in Sagittarius (late November)")
        
        response = requests.post(
            'http://localhost:8000/generate-chart',
            json=birth_data,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if response.status_code == 200:
            chart = response.json()
            
            print("\n" + "=" * 60)
            print("MIA'S CORRECTED NATAL CHART - COMPLETE JSON OUTPUT")
            print("=" * 60)
            
            # Pretty print the entire JSON response
            print(json.dumps(chart, indent=2, ensure_ascii=False))
            
            print("\n" + "=" * 60)
            print("CORRECTED CHART SUMMARY")
            print("=" * 60)
            
            # Extract key information
            sun_sign = chart.get('sunSign')
            ascendant = chart.get('ascendant', {})
            midheaven = chart.get('midheaven', {})
            chart_ruler = chart.get('chartRuler', {})
            
            print(f"Sun Sign: {sun_sign} (✓ Should be Sagittarius for Nov 22)")
            print(f"Ascendant: {ascendant.get('sign')} at {ascendant.get('exactDegree')}")
            print(f"Midheaven: {midheaven.get('sign')} at {midheaven.get('exactDegree')}")
            print(f"Chart Ruler: {chart_ruler.get('planet')} in {chart_ruler.get('sign')} (House {chart_ruler.get('house')})")
            print(f"House System: {chart.get('houseSystem')} (Whole Sign)")
            
            print("\nPLANETARY PLACEMENTS:")
            placements = chart.get('placements', [])
            
            for placement in placements:
                planet = placement.get('planet')
                sign = placement.get('sign')
                house = placement.get('house')
                exact_degree = placement.get('exactDegree')
                retrograde = placement.get('retrograde')
                
                retro_symbol = " ℞" if retrograde else ""
                print(f"  {planet}{retro_symbol}: {sign} {exact_degree} (House {house})")
            
        else:
            print(f"Error generating chart: {response.status_code}")
            error_detail = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            print(f"Error details: {error_detail}")
            
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Clean up
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    asyncio.run(generate_mia_correct_chart())