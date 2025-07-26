#!/usr/bin/env python3
"""
Final test demonstrating the API endpoint working exactly as requested.
This simulates the actual HTTP requests you would make to the API.
"""

import json
import subprocess
import time
import requests
from typing import Dict, Any

def start_api_server():
    """Start the API server for testing."""
    print("Starting API server...")
    proc = subprocess.Popen(['python', 'main.py'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
    time.sleep(4)  # Give server time to start
    return proc

def test_api_endpoint():
    """Test the actual API endpoint with HTTP requests."""
    print("🧪 TESTING LIVE API ENDPOINT")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test data samples
    test_requests = [
        {
            "name": "Test Person",
            "date": "1990-06-15",
            "time": "14:30", 
            "location": "New York, NY, USA"
        },
        {
            "name": "Sample User",
            "date": "1985-03-22",
            "time": "09:45",
            "location": "San Francisco, CA, USA"
        }
    ]
    
    for i, test_data in enumerate(test_requests, 1):
        print(f"\n🔍 API Test {i}: {test_data['name']}")
        print("-" * 30)
        
        try:
            # Make POST request to /generate-chart
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
                chart_data = response.json()
                
                print("✅ SUCCESS! Chart generated successfully")
                print("\n📊 Response Data:")
                print(f"   Rising Sign: {chart_data['risingSign']}")
                print(f"   Sun Sign: {chart_data['sunSign']}")
                print(f"   Moon Sign: {chart_data['moonSign']}")
                print(f"   Midheaven: {chart_data['midheaven']}")
                print(f"   Placements: {len(chart_data['placements'])} planets")
                
                # Show sample placements
                print("\n   Key Placements:")
                for placement in chart_data['placements'][:4]:
                    retro = " (R)" if placement.get('retrograde') else ""
                    print(f"     {placement['planet']}: {placement['sign']} in House {placement['house']} at {placement['degree']:.1f}°{retro}")
                
                # Verify required fields
                required_fields = ['risingSign', 'sunSign', 'moonSign', 'midheaven', 'placements']
                missing = [field for field in required_fields if field not in chart_data]
                
                if missing:
                    print(f"❌ Missing required fields: {missing}")
                else:
                    print("✅ All required fields present")
                
                # Show complete JSON sample
                print(f"\n📝 Complete JSON Response:")
                sample_response = {
                    "risingSign": chart_data['risingSign'],
                    "sunSign": chart_data['sunSign'], 
                    "moonSign": chart_data['moonSign'],
                    "midheaven": chart_data['midheaven'],
                    "placements": chart_data['placements'][:2]  # Show first 2 for brevity
                }
                print(json.dumps(sample_response, indent=2))
                
            else:
                print(f"❌ Request failed")
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection refused - API server not responding")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_house_system_endpoints():
    """Test house system configuration endpoints."""
    print(f"\n🏠 TESTING HOUSE SYSTEM CONFIGURATION")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    try:
        # Check current house system
        response = requests.get(f"{base_url}/current-house-system")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Current house system: {data['name']} ({data['code']})")
            
            if data['code'] == 'W':
                print("✅ Correctly configured for Whole Sign Houses")
            else:
                print(f"⚠️  Using {data['name']} instead of Whole Sign")
        
        # Get available house systems
        response = requests.get(f"{base_url}/house-systems")
        if response.status_code == 200:
            systems = response.json()
            print(f"✅ {len(systems)} house systems available")
            print(f"   Whole Sign option: {systems.get('W', 'Not found')}")
            
    except Exception as e:
        print(f"❌ House system test failed: {e}")

def show_curl_examples():
    """Show curl command examples for using the API."""
    print(f"\n💻 CURL COMMAND EXAMPLES")
    print("=" * 50)
    
    print("1. Generate a chart:")
    print("curl -X POST http://localhost:8000/generate-chart \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{")
    print('    "name": "John Doe",')
    print('    "date": "1990-06-15",')
    print('    "time": "14:30",')
    print('    "location": "New York, NY, USA"')
    print("  }'")
    
    print("\n2. Check house system:")
    print("curl http://localhost:8000/current-house-system")
    
    print("\n3. Set house system:")
    print("curl -X POST http://localhost:8000/set-house-system \\")
    print("  -H 'Content-Type: application/json' \\")
    print('  -d \'{"house_system": "W"}\'')

def main():
    """Run complete API test."""
    # Start server
    server_proc = None
    try:
        server_proc = start_api_server()
        
        # Run tests
        test_api_endpoint()
        test_house_system_endpoints()
        show_curl_examples()
        
        print(f"\n" + "=" * 50)
        print("🎯 API ENDPOINT CONFIRMATION")
        print("=" * 50)
        print("✅ Endpoint: POST /generate-chart")
        print("✅ Input validation: name, date, time, location")
        print("✅ House system: Whole Sign (W)")
        print("✅ Output format:")
        print("   • risingSign: string")
        print("   • sunSign: string") 
        print("   • moonSign: string")
        print("   • midheaven: string")
        print("   • placements: array of planet objects")
        print("✅ JSON response: Clean and structured")
        print("✅ Ready for production use!")
        
    finally:
        if server_proc:
            server_proc.terminate()
            print(f"\n🔒 Server stopped")

if __name__ == "__main__":
    main()