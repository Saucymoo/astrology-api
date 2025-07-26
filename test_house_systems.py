#!/usr/bin/env python3
"""
Test script to verify Whole Sign house system configuration.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_house_system_configuration():
    """Test house system endpoints and chart generation."""
    
    print("🔍 Testing Astrology API House System Configuration")
    print("=" * 60)
    
    # Test 1: Check current house system
    print("\n1️⃣ Checking current house system...")
    try:
        response = requests.get(f"{BASE_URL}/current-house-system")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Current house system: {data['name']} ({data['code']})")
            print(f"   Description: {data['description']}")
        else:
            print(f"❌ Failed to get current house system: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get available house systems
    print("\n2️⃣ Getting available house systems...")
    try:
        response = requests.get(f"{BASE_URL}/house-systems")
        if response.status_code == 200:
            systems = response.json()
            print("✅ Available house systems:")
            for code, name in systems.items():
                marker = "👉" if code == "W" else "  "
                print(f"   {marker} {code}: {name}")
        else:
            print(f"❌ Failed to get house systems: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Set house system to Whole Sign
    print("\n3️⃣ Setting house system to Whole Sign (W)...")
    try:
        response = requests.post(
            f"{BASE_URL}/set-house-system",
            json={"house_system": "W"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
        else:
            print(f"❌ Failed to set house system: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Generate a chart to verify house system
    print("\n4️⃣ Generating sample chart to verify Whole Sign houses...")
    try:
        chart_request = {
            "name": "Test Person",
            "date": "1990-06-15",
            "time": "14:30",
            "location": "New York, NY, USA"
        }
        
        response = requests.post(f"{BASE_URL}/generate-chart", json=chart_request)
        if response.status_code == 200:
            chart = response.json()
            print("✅ Chart generated successfully!")
            
            # Verify house system in response
            houses = chart.get("houses", [])
            if houses:
                print(f"   📊 Chart contains {len(houses)} houses")
                print("   🏠 House breakdown:")
                for house in houses[:6]:  # Show first 6 houses
                    print(f"      House {house['house']}: {house['sign']} at {house['degree']:.1f}°")
                
                # Check if degrees are 0.0 (typical for Whole Sign)
                zero_degree_houses = [h for h in houses if h['degree'] == 0.0]
                if len(zero_degree_houses) > 6:  # Most houses should start at 0° in Whole Sign
                    print("   ✅ Whole Sign pattern detected (most houses start at 0°)")
                else:
                    print("   ⚠️  Non-Whole Sign pattern (houses have varying degrees)")
                    
            # Show ascendant
            ascendant = chart.get("ascendant", {})
            if ascendant:
                print(f"   🌅 Rising sign: {ascendant['sign']} at {ascendant['degree']:.1f}°")
                
        else:
            print(f"❌ Failed to generate chart: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Test switching to different house system for comparison
    print("\n5️⃣ Testing house system switching (Placidus for comparison)...")
    try:
        # Switch to Placidus
        response = requests.post(
            f"{BASE_URL}/set-house-system",
            json={"house_system": "P"}
        )
        if response.status_code == 200:
            print("✅ Switched to Placidus temporarily")
            
            # Generate same chart with Placidus
            response = requests.post(f"{BASE_URL}/generate-chart", json=chart_request)
            if response.status_code == 200:
                chart = response.json()
                houses = chart.get("houses", [])
                print("   📊 Placidus house degrees:")
                for house in houses[:3]:
                    print(f"      House {house['house']}: {house['sign']} at {house['degree']:.1f}°")
        
        # Switch back to Whole Sign
        response = requests.post(
            f"{BASE_URL}/set-house-system",
            json={"house_system": "W"}
        )
        if response.status_code == 200:
            print("✅ Switched back to Whole Sign")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 House System Test Complete!")
    print("\n📝 Key Points:")
    print("   • House system is configurable via API endpoints")
    print("   • Default setting: Whole Sign Houses (W)")
    print("   • Setting persists across chart generations")
    print("   • Can be changed programmatically as needed")


def show_api_usage_examples():
    """Show practical examples of using the house system API."""
    
    print("\n" + "=" * 60)
    print("💡 Practical API Usage Examples")
    print("=" * 60)
    
    examples = {
        "Check current house system": {
            "method": "GET",
            "url": "/current-house-system",
            "description": "See what house system is currently active"
        },
        "Set Whole Sign houses": {
            "method": "POST", 
            "url": "/set-house-system",
            "body": {"house_system": "W"},
            "description": "Configure for Whole Sign houses"
        },
        "Set Placidus houses": {
            "method": "POST",
            "url": "/set-house-system", 
            "body": {"house_system": "P"},
            "description": "Configure for Placidus houses"
        },
        "Generate chart": {
            "method": "POST",
            "url": "/generate-chart",
            "body": {
                "name": "John Doe",
                "date": "1990-06-15",
                "time": "14:30", 
                "location": "New York, NY, USA"
            },
            "description": "Generate chart with current house system"
        }
    }
    
    for name, example in examples.items():
        print(f"\n🔸 {name}:")
        print(f"   {example['method']} {BASE_URL}{example['url']}")
        if 'body' in example:
            print(f"   Body: {json.dumps(example['body'], indent=2)}")
        print(f"   → {example['description']}")


if __name__ == "__main__":
    test_house_system_configuration()
    show_api_usage_examples()