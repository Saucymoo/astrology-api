"""
Test script for the Astrology Chart API.

This script demonstrates how to use the API to generate astrology charts
and can be used for testing and validation.
"""

import requests
import json
from datetime import datetime

# API configuration
API_BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Health check error: {e}")
    print()


def test_generate_chart():
    """Test generating an astrology chart."""
    print("Testing chart generation...")
    
    # Sample birth data
    birth_data = {
        "name": "John Doe",
        "date": "1990-06-15",
        "time": "14:30",
        "location": "New York, NY, USA"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate-chart",
            json=birth_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✓ Chart generation successful")
            data = response.json()
            
            print(f"  Name: {data['name']}")
            print(f"  Birth Date: {data['birth_info']['date']}")
            print(f"  Birth Time: {data['birth_info']['time']}")
            print(f"  Location: {data['birth_info']['location']}")
            print(f"  Coordinates: {data['birth_info']['latitude']}, {data['birth_info']['longitude']}")
            print(f"  Rising Sign: {data['ascendant']['sign']} at {data['ascendant']['degree']:.1f}°")
            
            print("\n  Key Planetary Positions:")
            for planet in data['planets'][:5]:  # Show first 5 planets
                print(f"    {planet['name']}: {planet['sign']} {planet['degree']:.1f}° (House {planet['house']})")
            
            print(f"\n  Total Planets: {len(data['planets'])}")
            print(f"  Total Houses: {len(data['houses'])}")
            
        else:
            print(f"✗ Chart generation failed: {response.status_code}")
            print(f"  Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Chart generation error: {e}")
    print()


def test_geocoding():
    """Test the geocoding endpoint."""
    print("Testing geocoding...")
    
    location_data = {"location": "Los Angeles, CA, USA"}
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/geocode",
            json=location_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✓ Geocoding successful")
            data = response.json()
            print(f"  Location: {data['location']}")
            print(f"  Coordinates: {data['latitude']}, {data['longitude']}")
            print(f"  Timezone: UTC{data['timezone']:+d}")
            print(f"  Full Name: {data.get('display_name', 'N/A')}")
        else:
            print(f"✗ Geocoding failed: {response.status_code}")
            print(f"  Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Geocoding error: {e}")
    print()


def test_metadata_endpoints():
    """Test metadata endpoints."""
    print("Testing metadata endpoints...")
    
    try:
        # Test planets endpoint
        response = requests.get(f"{API_BASE_URL}/planets")
        if response.status_code == 200:
            planets = response.json()
            print(f"✓ Planets endpoint: {len(planets)} planets supported")
            print(f"  Examples: {', '.join(planets[:5])}")
        else:
            print(f"✗ Planets endpoint failed: {response.status_code}")
        
        # Test zodiac signs endpoint
        response = requests.get(f"{API_BASE_URL}/zodiac-signs")
        if response.status_code == 200:
            signs = response.json()
            print(f"✓ Zodiac signs endpoint: {len(signs)} signs")
            print(f"  All signs: {', '.join(signs)}")
        else:
            print(f"✗ Zodiac signs endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Metadata endpoints error: {e}")
    print()


def run_full_test():
    """Run all tests."""
    print("=" * 60)
    print("ASTROLOGY CHART API - TEST SUITE")
    print("=" * 60)
    print()
    
    test_health_check()
    test_metadata_endpoints()
    test_geocoding()
    test_generate_chart()
    
    print("=" * 60)
    print("TEST SUITE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    print("Astrology Chart API Test Script")
    print("Make sure the API server is running on http://localhost:8000")
    print()
    
    choice = input("Run full test suite? (y/n): ").lower().strip()
    if choice == 'y' or choice == 'yes':
        run_full_test()
    else:
        print("Individual test options:")
        print("1. Health check")
        print("2. Generate chart")
        print("3. Geocoding")
        print("4. Metadata endpoints")
        
        test_choice = input("Enter test number (1-4): ").strip()
        
        if test_choice == "1":
            test_health_check()
        elif test_choice == "2":
            test_generate_chart()
        elif test_choice == "3":
            test_geocoding()
        elif test_choice == "4":
            test_metadata_endpoints()
        else:
            print("Invalid choice. Running full test suite...")
            run_full_test()