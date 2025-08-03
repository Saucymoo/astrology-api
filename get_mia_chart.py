#!/usr/bin/env python3
"""
Get Mia's corrected natal chart with proper date format.
"""

import requests
import json
from datetime import datetime

def get_mia_chart():
    """Get Mia's natal chart with corrected date format."""
    
    print("=" * 60)
    print("MIA'S CORRECTED NATAL CHART")
    print("Date Format Fixed: DD/MM/YYYY Now Supported")
    print("=" * 60)
    
    # Mia's corrected birth data
    birth_data = {
        'name': 'Mia',
        'date': '22/11/1974',  # DD/MM/YYYY - November 22, 1974
        'time': '19:10',
        'location': 'Adelaide, South Australia, Australia'
    }
    
    print("Birth Information:")
    print(f"  Name: {birth_data['name']}")
    print(f"  Date: {birth_data['date']} (DD/MM/YYYY format)")
    print(f"  Interpreted as: November 22, 1974")
    print(f"  Time: {birth_data['time']}")
    print(f"  Location: {birth_data['location']}")
    
    try:
        # Make API call
        response = requests.post(
            'http://localhost:8000/generate-chart',
            json=birth_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            chart = response.json()
            
            print("\n" + "=" * 60)
            print("COMPLETE NATAL CHART JSON")
            print("=" * 60)
            
            # Pretty print JSON
            print(json.dumps(chart, indent=2, ensure_ascii=False))
            
            print("\n" + "=" * 60)
            print("CHART SUMMARY")
            print("=" * 60)
            
            # Key information
            sun_sign = chart.get('sunSign')
            rising_sign = chart.get('risingSign')
            moon_sign = chart.get('moonSign')
            
            ascendant = chart.get('ascendant', {})
            midheaven = chart.get('midheaven', {})
            chart_ruler = chart.get('chartRuler', {})
            
            print(f"Sun: {sun_sign}")
            print(f"Rising: {rising_sign}")
            print(f"Moon: {moon_sign}")
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
            
            return chart
            
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Connection error: {e}")
        print("Make sure the Python API server is running on port 8000")
        return None

if __name__ == "__main__":
    # Start a simple server inline for testing
    import subprocess
    import time
    import sys
    
    print("Starting Python API server...")
    proc = subprocess.Popen([sys.executable, 'main.py'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        chart = get_mia_chart()
    finally:
        proc.terminate()
        proc.wait()