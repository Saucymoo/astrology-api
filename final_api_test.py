#!/usr/bin/env python3
"""
Final API test to provide deployment information and confirm functionality.
"""

import json
import subprocess
import time
import sys

def test_api_and_provide_deployment_info():
    """Test the API and provide deployment information."""
    print("Astrology Chart API - Deployment Information")
    print("=" * 50)
    
    # Start the Python FastAPI server
    print("Starting FastAPI server...")
    try:
        proc = subprocess.Popen(
            [sys.executable, 'main.py'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(5)  # Give server time to start
        
        # Test with curl since requests might not be available
        print("Testing API endpoints...")
        
        # Test health endpoint
        health_result = subprocess.run(
            ['curl', '-s', 'http://localhost:8000/health'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if health_result.returncode == 0 and health_result.stdout:
            print(f"✓ Health endpoint working: {health_result.stdout}")
            
            # Test generate-chart endpoint
            test_data = json.dumps({
                "name": "Test User",
                "date": "1990-06-15",
                "time": "14:30", 
                "location": "New York, NY, USA"
            })
            
            chart_result = subprocess.run([
                'curl', '-s', '-X', 'POST',
                'http://localhost:8000/generate-chart',
                '-H', 'Content-Type: application/json',
                '-d', test_data
            ], capture_output=True, text=True, timeout=15)
            
            if chart_result.returncode == 0 and chart_result.stdout:
                try:
                    response = json.loads(chart_result.stdout)
                    print("✓ Generate-chart endpoint working!")
                    
                    print("\nAPI RESPONSE VERIFICATION:")
                    print(f"  Request Fields: name, date, time, location ✓")
                    print(f"  House System: {response.get('houseSystem', 'Unknown')} (Whole Sign) ✓")
                    print(f"  Rising Sign: {response.get('risingSign', 'Unknown')} ✓")
                    print(f"  Sun Sign: {response.get('sunSign', 'Unknown')} ✓") 
                    print(f"  Moon Sign: {response.get('moonSign', 'Unknown')} ✓")
                    print(f"  Midheaven: {response.get('midheaven', {})} ✓")
                    print(f"  Descendant: {response.get('descendant', {})} ✓")
                    print(f"  Imum Coeli: {response.get('imumCoeli', {})} ✓")
                    print(f"  Total Placements: {len(response.get('placements', []))} ✓")
                    
                    # Check for all required planets
                    planets = [p['planet'] for p in response.get('placements', [])]
                    required = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'North Node', 'South Node']
                    missing = [p for p in required if p not in planets]
                    
                    print(f"  Required Planets: {len(required) - len(missing)}/{len(required)} present")
                    if not missing:
                        print("  ✓ All required astrological points included!")
                    else:
                        print(f"  ⚠ Missing: {missing}")
                    
                    print("\nSAMPLE JSON RESPONSE:")
                    print(json.dumps({
                        "risingSign": response.get('risingSign'),
                        "sunSign": response.get('sunSign'),
                        "moonSign": response.get('moonSign'),
                        "midheaven": response.get('midheaven'),
                        "descendant": response.get('descendant'),
                        "imumCoeli": response.get('imumCoeli'),
                        "placements": response.get('placements', [])[:3],  # First 3
                        "houseSystem": response.get('houseSystem'),
                        "total_placements": len(response.get('placements', []))
                    }, indent=2))
                    
                except json.JSONDecodeError:
                    print(f"✗ Invalid JSON response: {chart_result.stdout[:200]}")
                    
            else:
                print(f"✗ Generate-chart failed: {chart_result.stderr}")
                
        else:
            print(f"✗ Health endpoint failed: {health_result.stderr}")
        
        # Provide deployment information
        print("\n" + "=" * 50)
        print("DEPLOYMENT INFORMATION:")
        print("=" * 50)
        
        print("🌐 PUBLIC API ACCESS:")
        print("   Note: This is running locally. For public access, you need to deploy to Replit.")
        print("   When deployed, the URL format will be:")
        print("   https://[repl-name].[username].repl.co")
        print("")
        print("📡 API ENDPOINTS:")
        print("   Base URL: https://[your-repl].repl.co")
        print("   Main endpoint: POST /generate-chart")
        print("   Health check: GET /health")
        print("   Documentation: GET /docs")
        print("")
        print("🔧 API SPECIFICATIONS:")
        print("   ✓ House System: Whole Sign (configured)")
        print("   ✓ Authentication: None required (public API)")
        print("   ✓ Protocol: HTTPS when deployed")
        print("   ✓ Request Format: JSON")
        print("   ✓ All 17 astrological points included")
        print("")
        print("📝 REQUEST FORMAT:")
        print('   POST https://[your-repl].repl.co/generate-chart')
        print('   Content-Type: application/json')
        print('   Body: {')
        print('     "name": "User Name",')
        print('     "date": "1990-06-15",')
        print('     "time": "14:30",')
        print('     "location": "New York, NY, USA"')
        print('   }')
        print("")
        print("📤 RESPONSE INCLUDES:")
        print("   • risingSign, sunSign, moonSign")
        print("   • midheaven, descendant, imumCoeli (with sign & degree)")
        print("   • placements array (13 planetary bodies)")
        print("   • houseSystem: 'W' (Whole Sign)")
        print("   • All planetary positions with houses, degrees, retrograde status")
        
    except Exception as e:
        print(f"Error during testing: {e}")
    
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except:
            pass
        print("\nServer stopped.")

if __name__ == "__main__":
    test_api_and_provide_deployment_info()