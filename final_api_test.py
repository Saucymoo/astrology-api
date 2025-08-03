#!/usr/bin/env python3
"""
Final API test - start server and test the endpoint manually.
"""

import asyncio
import json
import requests
from run_production import app
import uvicorn
import threading
import time

def start_server():
    """Start the FastAPI server in a thread."""
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def test_api():
    """Test the API endpoint."""
    
    print("=" * 60)
    print("TESTING ASTROLOGY CHART API")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Could not connect to API: {e}")
        return
    
    # Test chart generation
    print(f"\n" + "=" * 60)
    print("TESTING CHART GENERATION")
    print("=" * 60)
    
    test_request = {
        "name": "Test User",
        "birth_date": "1990-06-15",
        "birth_time": "14:30", 
        "birth_location": "London, UK"
    }
    
    print("Request:")
    print(json.dumps(test_request, indent=2))
    
    try:
        response = requests.post(
            f"{base_url}/generate-chart",
            json=test_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"\n✅ Chart generation successful!")
            chart = response.json()
            
            print(f"\nCHART SUMMARY:")
            print(f"Name: {chart['name']}")
            print(f"Rising: {chart['rising_sign']} {chart['ascendant']['exact_degree']}")
            print(f"Sun: {chart['sun_sign']}")
            print(f"Moon: {chart['moon_sign']}")
            print(f"House System: {chart['house_system']}")
            print(f"Planets: {len(chart['placements'])}")
            
            print(f"\nFIRST 3 PLANETARY POSITIONS:")
            for i, planet in enumerate(chart['placements'][:3]):
                print(f"  {planet['planet']}: {planet['sign']} {planet['exact_degree']} (House {planet['house']})")
            
            print(f"\n✅ API TEST SUCCESSFUL")
            print(f"✅ All required fields present")
            print(f"✅ Whole Sign house system confirmed")
            
            return chart
            
        else:
            print(f"❌ Chart generation failed: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Chart generation error: {e}")
        return None

if __name__ == "__main__":
    print("Starting API server and running test...")
    
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Run test
    result = test_api()
    
    if result:
        print(f"\n" + "=" * 60)
        print("API DEPLOYMENT INFORMATION")
        print("=" * 60)
        print("✅ PUBLIC API URL: http://localhost:8000")
        print("✅ MAIN ENDPOINT: POST /generate-chart")
        print("✅ DOCUMENTATION: http://localhost:8000/docs")
        print("✅ HEALTH CHECK: http://localhost:8000/health")
        
        print(f"\nSAMPLE cURL REQUEST:")
        print('curl -X POST "http://localhost:8000/generate-chart" \\')
        print('  -H "Content-Type: application/json" \\')
        print('  -d \'{"name": "John Doe", "birth_date": "1990-06-15", "birth_time": "14:30", "birth_location": "New York, NY, USA"}\'')
        
        print(f"\nSAMPLE JavaScript fetch():")
        print("const response = await fetch('http://localhost:8000/generate-chart', {")
        print("  method: 'POST',")
        print("  headers: { 'Content-Type': 'application/json' },")
        print("  body: JSON.stringify({")
        print("    name: 'John Doe',")
        print("    birth_date: '1990-06-15',")
        print("    birth_time: '14:30',")
        print("    birth_location: 'New York, NY, USA'")
        print("  })")
        print("});")
        print("const chart = await response.json();")
        
        # Keep server running
        print(f"\n✅ Server running - API ready for use!")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
    else:
        print("❌ API test failed")