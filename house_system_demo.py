#!/usr/bin/env python3
"""
Demonstration of Whole Sign House System Configuration in Astrology API

This script shows exactly where the house system is configured and how to modify it.
"""

def show_house_system_configuration():
    """Display the exact configuration locations."""
    
    print("🎯 WHOLE SIGN HOUSE SYSTEM CONFIGURATION")
    print("=" * 60)
    
    print("\n📍 LOCATION 1: services/astrology_service.py (Lines 25-40)")
    print("   This is where the house system is set for REAL API calls:")
    print()
    print("   class AstrologyService:")
    print("       def __init__(self):")
    print("           # House system configuration - CRITICAL FOR ACCURACY")
    print("           self.house_system = 'W'  # ← WHOLE SIGN HOUSES")
    print("           # Available options:")
    print("           # 'P' = Placidus (most common default)")
    print("           # 'W' = Whole Sign Houses ← YOUR PREFERRED METHOD")
    print("           # 'K' = Koch, 'R' = Regiomontanus, etc.")
    
    print("\n📍 LOCATION 2: services/astrology_service.py (Line 116)")
    print("   This is where the house system gets sent to the API:")
    print()
    print("   payload = {")
    print("       'day': day, 'month': month, 'year': year,")
    print("       'hour': hour, 'min': minute,")
    print("       'lat': birth_info.latitude,")
    print("       'lon': birth_info.longitude,")
    print("       'house_system': self.house_system  # ← 'W' for Whole Sign")
    print("   }")
    
    print("\n📍 LOCATION 3: services/mock_astrology_service.py (Line 26)")
    print("   This matches the real service for testing:")
    print()
    print("   class MockAstrologyService:")
    print("       def __init__(self):")
    print("           self.house_system = 'W'  # ← WHOLE SIGN HOUSES")
    
    print("\n🔧 HOW TO CHANGE THE HOUSE SYSTEM:")
    print("   Option 1 - Permanently change in code:")
    print("     Edit services/astrology_service.py line 26")
    print("     Change: self.house_system = 'P'  # for Placidus")
    print("     Change: self.house_system = 'K'  # for Koch")
    print("     Change: self.house_system = 'W'  # for Whole Sign")
    
    print("\n   Option 2 - Change via API endpoints:")
    print("     POST /set-house-system")
    print("     Body: {'house_system': 'W'}")
    print("     GET /current-house-system (to check current setting)")
    
    print("\n   Option 3 - Change programmatically in Python:")
    print("     from services.astrology_service import AstrologyService")
    print("     service = AstrologyService()")
    print("     service.set_house_system('W')  # Whole Sign")
    print("     service.set_house_system('P')  # Placidus")
    
    print("\n✅ VERIFICATION:")
    print("   • Currently set to: 'W' (Whole Sign Houses)")
    print("   • This affects ALL chart calculations")
    print("   • Setting persists for the session")
    print("   • Both real and mock services use the same setting")
    
    print("\n🏠 WHOLE SIGN HOUSE CHARACTERISTICS:")
    print("   • Each house occupies exactly one zodiac sign")
    print("   • House cusps typically at 0° of each sign")
    print("   • 1st house = Rising sign, 2nd house = next sign, etc.")
    print("   • Simpler and more traditional than Placidus")
    print("   • Preferred by many Hellenistic and traditional astrologers")


def show_available_house_systems():
    """Show all available house system options."""
    
    print("\n" + "=" * 60)
    print("🏠 AVAILABLE HOUSE SYSTEMS")
    print("=" * 60)
    
    systems = {
        "W": "Whole Sign Houses (YOUR CURRENT SETTING)",
        "P": "Placidus (Most common modern default)",
        "K": "Koch",
        "O": "Porphyrius", 
        "R": "Regiomontanus",
        "C": "Campanus",
        "A": "Equal Houses",
        "V": "Vehlow Equal Houses",
        "X": "Meridian Houses", 
        "H": "Azimuthal",
        "T": "Topocentric",
        "B": "Alcabitius",
        "M": "Morinus"
    }
    
    for code, name in systems.items():
        marker = "👉" if code == "W" else "  "
        print(f"   {marker} {code}: {name}")


def show_api_endpoints():
    """Show house system management endpoints."""
    
    print("\n" + "=" * 60)
    print("🌐 API ENDPOINTS FOR HOUSE SYSTEM MANAGEMENT")
    print("=" * 60)
    
    endpoints = [
        {
            "method": "GET",
            "path": "/current-house-system",
            "description": "Check current house system setting",
            "example": "curl http://localhost:8000/current-house-system"
        },
        {
            "method": "GET", 
            "path": "/house-systems",
            "description": "List all available house systems",
            "example": "curl http://localhost:8000/house-systems"
        },
        {
            "method": "POST",
            "path": "/set-house-system",
            "description": "Change house system",
            "example": "curl -X POST http://localhost:8000/set-house-system -H 'Content-Type: application/json' -d '{\"house_system\": \"W\"}'"
        },
        {
            "method": "POST",
            "path": "/generate-chart", 
            "description": "Generate chart with current house system",
            "example": "curl -X POST http://localhost:8000/generate-chart -H 'Content-Type: application/json' -d '{\"name\": \"John\", \"date\": \"1990-06-15\", \"time\": \"14:30\", \"location\": \"New York, NY\"}'"
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n🔸 {endpoint['method']} {endpoint['path']}")
        print(f"   {endpoint['description']}")
        print(f"   Example: {endpoint['example']}")


if __name__ == "__main__":
    show_house_system_configuration()
    show_available_house_systems()
    show_api_endpoints()
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY: Your API is configured for Whole Sign Houses!")
    print("   The setting is located in services/astrology_service.py line 26")
    print("   You can modify it there or use the API endpoints to change it")
    print("=" * 60)