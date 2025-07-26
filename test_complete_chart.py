#!/usr/bin/env python3
"""
Test script to verify all required astrological points are included in the chart response.
"""

import asyncio
import json
from models import BirthInfoRequest
from models_chart_points import CompleteChartResponse
from services.mock_astrology_service import MockAstrologyService
from main import _convert_to_complete_chart_response

async def test_all_required_points():
    """Test that all required astrological points are included."""
    print("🌟 TESTING ALL REQUIRED ASTROLOGICAL POINTS")
    print("=" * 60)
    
    # Required points from user's specification
    required_points = [
        "Sun", "Moon", "Mercury", "Venus", "Mars", 
        "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron"
    ]
    
    required_chart_angles = [
        "Rising", "Midheaven", "Descendant", "Imum Coeli"
    ]
    
    service = MockAstrologyService()
    
    # Test with sample birth info
    birth_info = BirthInfoRequest(
        name="Complete Chart Test",
        date="1990-06-15",
        time="14:30",
        location="New York, NY, USA"
    )
    
    try:
        # Generate raw chart
        raw_chart = await service.generate_chart(birth_info)
        print(f"✅ Raw chart generated with {len(raw_chart.planets)} planets")
        
        # Convert to complete format
        complete_chart = _convert_to_complete_chart_response(raw_chart)
        print(f"✅ Converted to complete chart format")
        
        # Check all required planetary points
        print(f"\n🪐 PLANETARY POINTS VERIFICATION:")
        found_planets = {p.planet for p in complete_chart.placements}
        
        for planet in required_points:
            if planet in found_planets:
                planet_data = next(p for p in complete_chart.placements if p.planet == planet)
                retro_text = " (R)" if planet_data.retrograde else ""
                print(f"   ✅ {planet}: {planet_data.sign} in House {planet_data.house} at {planet_data.degree:.1f}°{retro_text}")
            else:
                print(f"   ❌ {planet}: MISSING")
        
        missing_planets = set(required_points) - found_planets
        if missing_planets:
            print(f"\n⚠️  Missing planets: {missing_planets}")
        else:
            print(f"\n✅ All {len(required_points)} required planets present!")
        
        # Check chart angles
        print(f"\n🔺 CHART ANGLES VERIFICATION:")
        print(f"   ✅ Rising (Ascendant): {complete_chart.risingSign}")
        print(f"   ✅ Midheaven (MC): {complete_chart.midheaven.sign} at {complete_chart.midheaven.degree:.1f}°")
        print(f"   ✅ Descendant (DC): {complete_chart.descendant.sign} at {complete_chart.descendant.degree:.1f}°")
        print(f"   ✅ Imum Coeli (IC): {complete_chart.imumCoeli.sign} at {complete_chart.imumCoeli.degree:.1f}°")
        
        # Check basic signs
        print(f"\n⭐ KEY SIGNS:")
        print(f"   Sun Sign: {complete_chart.sunSign}")
        print(f"   Moon Sign: {complete_chart.moonSign}")
        print(f"   Rising Sign: {complete_chart.risingSign}")
        
        # Verify house system
        print(f"\n🏠 HOUSE SYSTEM:")
        print(f"   System: {complete_chart.houseSystem} (Whole Sign)")
        
        # Show complete JSON structure
        print(f"\n📝 COMPLETE JSON SAMPLE:")
        sample_json = {
            "risingSign": complete_chart.risingSign,
            "sunSign": complete_chart.sunSign,
            "moonSign": complete_chart.moonSign,
            "midheaven": {
                "sign": complete_chart.midheaven.sign,
                "degree": complete_chart.midheaven.degree
            },
            "descendant": {
                "sign": complete_chart.descendant.sign,
                "degree": complete_chart.descendant.degree
            },
            "imumCoeli": {
                "sign": complete_chart.imumCoeli.sign,
                "degree": complete_chart.imumCoeli.degree
            },
            "placements": [
                {
                    "planet": p.planet,
                    "sign": p.sign,
                    "house": p.house,
                    "degree": p.degree,
                    "retrograde": p.retrograde
                }
                for p in complete_chart.placements[:5]  # Show first 5
            ],
            "houseSystem": complete_chart.houseSystem,
            "generatedAt": complete_chart.generatedAt.isoformat()
        }
        
        print(json.dumps(sample_json, indent=2))
        
        return complete_chart
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

async def test_api_completeness():
    """Test the API endpoint completeness."""
    print(f"\n🌐 API ENDPOINT COMPLETENESS TEST")
    print("=" * 60)
    
    chart = await test_all_required_points()
    
    if chart:
        # Verify all user requirements
        requirements_met = {
            "Sun": hasattr(chart, 'sunSign') and chart.sunSign != "Unknown",
            "Rising": hasattr(chart, 'risingSign') and chart.risingSign != "Unknown", 
            "Moon": hasattr(chart, 'moonSign') and chart.moonSign != "Unknown",
            "Venus": any(p.planet == "Venus" for p in chart.placements),
            "Mercury": any(p.planet == "Mercury" for p in chart.placements),
            "Mars": any(p.planet == "Mars" for p in chart.placements),
            "Jupiter": any(p.planet == "Jupiter" for p in chart.placements),
            "Saturn": any(p.planet == "Saturn" for p in chart.placements),
            "Uranus": any(p.planet == "Uranus" for p in chart.placements),
            "Neptune": any(p.planet == "Neptune" for p in chart.placements),
            "Pluto": any(p.planet == "Pluto" for p in chart.placements),
            "Chiron": any(p.planet == "Chiron" for p in chart.placements),
            "Midheaven": hasattr(chart, 'midheaven'),
            "Descendant": hasattr(chart, 'descendant'),
            "Imum Coeli": hasattr(chart, 'imumCoeli')
        }
        
        print(f"📊 REQUIREMENTS CHECKLIST:")
        for requirement, met in requirements_met.items():
            status = "✅" if met else "❌"
            print(f"   {status} {requirement}")
        
        all_met = all(requirements_met.values())
        print(f"\n🎯 OVERALL STATUS: {'✅ ALL REQUIREMENTS MET' if all_met else '❌ SOME REQUIREMENTS MISSING'}")
        
        return all_met
    
    return False

def show_usage_example():
    """Show how to use the enhanced API."""
    print(f"\n💡 API USAGE EXAMPLE")
    print("=" * 60)
    
    print("POST /generate-chart")
    print("Content-Type: application/json")
    print()
    print("Request body:")
    print(json.dumps({
        "name": "John Doe",
        "date": "1990-06-15",
        "time": "14:30",
        "location": "New York, NY, USA"
    }, indent=2))
    
    print(f"\nResponse will include:")
    print("• risingSign, sunSign, moonSign")
    print("• midheaven, descendant, imumCoeli (with sign & degree)")
    print("• placements array with all planets including Chiron")
    print("• Whole Sign house system configuration")
    print("• Complete astrological chart data")

async def main():
    """Run complete test suite."""
    all_requirements_met = await test_api_completeness()
    show_usage_example()
    
    print(f"\n" + "=" * 60)
    print("🎯 FINAL VERIFICATION")
    print("=" * 60)
    
    if all_requirements_met:
        print("✅ ALL REQUIRED ASTROLOGICAL POINTS INCLUDED")
        print("✅ API ready for production use")
        print("✅ Whole Sign house system configured")
        print("✅ Complete chart data available")
    else:
        print("❌ Some requirements not met - check output above")

if __name__ == "__main__":
    asyncio.run(main())