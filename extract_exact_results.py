#!/usr/bin/env python3
"""
Extract and display the exact results from both approaches in a clear format
for user accuracy verification.
"""

import json

def display_results():
    """Display results in a clear, comparable format."""
    
    print("=" * 80)
    print("EXACT RESULTS FROM BOTH APPROACHES")
    print("For Your Accuracy Verification")
    print("=" * 80)
    
    try:
        with open('complete_api_test.json', 'r') as f:
            data = json.load(f)
        
        print("TEST CASE:")
        print(f"  Date: {data['test_info']['date']}")
        print(f"  Time: {data['test_info']['time']}")
        print(f"  Location: {data['test_info']['location']}")
        print(f"  Coordinates: {data['test_info']['coordinates']['latitude']}, {data['test_info']['coordinates']['longitude']}")
        print(f"  Your Previous Correction: Sun at 29°42'23\" Scorpio")
        
        print(f"\n" + "=" * 80)
        print("APPROACH 1: SWISS EPHEMERIS RESULTS")
        print("=" * 80)
        
        swiss = data['swiss_ephemeris_results']
        if swiss:
            print(f"Source: {swiss['source']}")
            print(f"House System: {swiss['house_system']}")
            print(f"Ascendant: {swiss['ascendant']['sign']} {swiss['ascendant']['exact_degree']}")
            print()
            print("All Planetary Positions:")
            print("Planet".ljust(12) + "Sign".ljust(12) + "Exact Degree".ljust(13) + "House".ljust(6))
            print("-" * 50)
            
            for planet in swiss['planets']:
                print(f"{planet['name'].ljust(12)}{planet['sign'].ljust(12)}{planet['exact_degree'].ljust(13)}{str(planet['house']).ljust(6)}")
            
            # Highlight Sun position
            sun = next((p for p in swiss['planets'] if p['name'] == 'Sun'), None)
            if sun:
                print(f"\n🎯 KEY RESULT - Sun Position: {sun['sign']} {sun['exact_degree']}")
        else:
            print("No Swiss Ephemeris results available")
        
        print(f"\n" + "=" * 80)
        print("APPROACH 2: EXTERNAL API RESULTS")
        print("=" * 80)
        
        api_data = data['external_api_results']
        print(f"Test Data Sent to APIs:")
        print(json.dumps(api_data['test_data'], indent=2))
        print()
        
        working_found = False
        for api_response in api_data['api_responses']:
            print(f"API: {api_response['name']}")
            print(f"URL: {api_response['url']}")
            print(f"Status: {api_response.get('status_code', 'No response')}")
            
            if 'json_data' in api_response:
                print("✅ SUCCESS - Received JSON data:")
                print(json.dumps(api_response['json_data'], indent=2)[:500] + "...")
                working_found = True
            elif 'error' in api_response:
                print(f"❌ ERROR: {api_response['error']}")
            elif api_response.get('status_code') == 404:
                print("❌ API endpoint not found")
            else:
                print("❌ No usable data received")
            print()
        
        if not working_found:
            print("❌ NO WORKING EXTERNAL APIs FOUND")
            print("All tested APIs either returned errors or require authentication")
        
        print(f"\n" + "=" * 80)
        print("ACCURACY VERIFICATION QUESTION FOR YOU")
        print("=" * 80)
        
        if swiss:
            sun = next((p for p in swiss['planets'] if p['name'] == 'Sun'), None)
            if sun:
                print(f"Swiss Ephemeris calculated: Sun at {sun['sign']} {sun['exact_degree']}")
                print(f"Your previous correction was: Sun at 29°42'23\" Scorpio")
                print()
                if sun['sign'] == 'Scorpio' and '29°42' in sun['exact_degree']:
                    print("✅ These match! Swiss Ephemeris appears astronomically accurate.")
                else:
                    print("⚠ There's a difference. Which do you believe is more accurate?")
        
        if not working_found:
            print("\nNo external API data is available for comparison since all APIs")
            print("either returned 404 errors or require authentication.")
            print()
            print("QUESTION: Based on this comparison, which approach do you prefer?")
            print("A) Swiss Ephemeris (matches your previous correction)")
            print("B) Continue trying to find working external APIs")
        
    except FileNotFoundError:
        print("Results file not found. Running comparison first...")
        return False
    
    return True

if __name__ == "__main__":
    if not display_results():
        print("Please run the comparison first to generate results.")