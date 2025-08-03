#!/usr/bin/env python3
"""
Generate a sample full natal chart output to show the complete API response structure.
"""

import asyncio
import json
import subprocess
import time
import sys
import requests

async def generate_sample_chart():
    """Generate and display a complete natal chart in structured JSON format."""
    
    print("GENERATING FULL NATAL CHART OUTPUT")
    print("=" * 60)
    
    # Start the server
    proc = subprocess.Popen([sys.executable, 'main.py'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Generate chart for a specific birth data
        birth_data = {
            'name': 'Sample Chart',
            'date': '1990-06-15',
            'time': '14:30',
            'location': 'New York, NY, USA'
        }
        
        print(f"Birth Data: {birth_data}")
        print("\nGenerating chart...")
        
        response = requests.post(
            'http://localhost:8000/generate-chart',
            json=birth_data,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if response.status_code == 200:
            chart = response.json()
            
            print("\n" + "=" * 60)
            print("COMPLETE NATAL CHART OUTPUT (JSON)")
            print("=" * 60)
            
            # Pretty print the entire JSON response
            print(json.dumps(chart, indent=2, ensure_ascii=False))
            
            print("\n" + "=" * 60)
            print("PLANETARY BREAKDOWN")
            print("=" * 60)
            
            # Extract and display planetary information in structured format
            placements = chart.get('placements', [])
            
            for placement in placements:
                planet = placement.get('planet')
                sign = placement.get('sign')
                house = placement.get('house')
                exact_degree = placement.get('exactDegree')
                retrograde = placement.get('retrograde')
                house_ruler = placement.get('houseRuler')
                
                retro_symbol = " ℞" if retrograde else ""
                print(f"{planet}{retro_symbol}:")
                print(f"  Sign: {sign}")
                print(f"  Exact Degree: {exact_degree}")
                print(f"  House: {house}")
                print(f"  House Ruler: {house_ruler}")
                print()
            
            # Confirm house system
            house_system = chart.get('houseSystem')
            print(f"House System Confirmation: '{house_system}' (W = Whole Sign)")
            
        else:
            print(f"Error generating chart: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Clean up
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    asyncio.run(generate_sample_chart())