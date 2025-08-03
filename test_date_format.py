#!/usr/bin/env python3
"""
Test different date formats to ensure correct interpretation.
"""

import asyncio
import json
import subprocess
import time
import sys
import requests

async def test_date_formats():
    """Test both date formats for Mia's birth data."""
    
    print("TESTING DATE FORMATS FOR MIA'S CHART")
    print("=" * 60)
    
    # Start the server
    proc = subprocess.Popen([sys.executable, 'main.py'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Test 1: ISO format (YYYY-MM-DD) - should be November 22, 1974
        birth_data_iso = {
            'name': 'Mia',
            'date': '1974-11-22',  # ISO format: November 22, 1974
            'time': '19:10',
            'location': 'Adelaide, South Australia, Australia'
        }
        
        print("Test 1: ISO Format (1974-11-22) - November 22, 1974")
        print("Expected: Sun in Sagittarius (late November)")
        
        response1 = requests.post(
            'http://localhost:8000/generate-chart',
            json=birth_data_iso,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if response1.status_code == 200:
            chart1 = response1.json()
            sun_sign1 = chart1.get('sunSign')
            print(f"Result: Sun in {sun_sign1}")
        
        # Test 2: DD/MM/YYYY format if supported
        birth_data_ddmm = {
            'name': 'Mia',
            'date': '22/11/1974',  # DD/MM/YYYY format: November 22, 1974
            'time': '19:10',
            'location': 'Adelaide, South Australia, Australia'
        }
        
        print("\nTest 2: DD/MM/YYYY Format (22/11/1974) - November 22, 1974")
        print("Expected: Sun in Sagittarius (late November)")
        
        response2 = requests.post(
            'http://localhost:8000/generate-chart',
            json=birth_data_ddmm,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if response2.status_code == 200:
            chart2 = response2.json()
            sun_sign2 = chart2.get('sunSign')
            print(f"Result: Sun in {sun_sign2}")
        else:
            print(f"DD/MM/YYYY format failed: {response2.status_code}")
        
        # Test 3: Alternative format
        birth_data_alt = {
            'name': 'Mia',
            'date': '22-11-1974',  # DD-MM-YYYY format
            'time': '19:10',
            'location': 'Adelaide, South Australia, Australia'
        }
        
        print("\nTest 3: DD-MM-YYYY Format (22-11-1974) - November 22, 1974")
        
        response3 = requests.post(
            'http://localhost:8000/generate-chart',
            json=birth_data_alt,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if response3.status_code == 200:
            chart3 = response3.json()
            sun_sign3 = chart3.get('sunSign')
            print(f"Result: Sun in {sun_sign3}")
        else:
            print(f"DD-MM-YYYY format failed: {response3.status_code}")
        
        print("\n" + "=" * 60)
        print("DATE FORMAT ANALYSIS")
        print("=" * 60)
        print("November 22, 1974 should place the Sun in SAGITTARIUS")
        print("(Sun enters Sagittarius around November 22-23)")
        print()
        print("If we're getting Libra, the date is being interpreted incorrectly")
        print("Libra season: September 23 - October 22")
        print("This suggests the date might be interpreted as February 11th instead")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Clean up
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    asyncio.run(test_date_formats())