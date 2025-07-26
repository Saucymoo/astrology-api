#!/usr/bin/env python3
"""
Test to verify North Node and South Node are included in the chart response.
"""

import asyncio
import json
from models import BirthInfoRequest
from services.mock_astrology_service import MockAstrologyService
from main import _convert_to_complete_chart_response

async def test_lunar_nodes():
    """Test that North Node and South Node are included."""
    print("🌙 TESTING LUNAR NODES INCLUSION")
    print("=" * 50)
    
    service = MockAstrologyService()
    
    birth_info = BirthInfoRequest(
        name="Nodes Test",
        date="1990-06-15",
        time="14:30",
        location="New York, NY, USA"
    )
    
    try:
        # Generate chart
        raw_chart = await service.generate_chart(birth_info)
        complete_chart = _convert_to_complete_chart_response(raw_chart)
        
        # Check for lunar nodes
        found_planets = {p.planet for p in complete_chart.placements}
        
        print("🔍 CHECKING FOR LUNAR NODES:")
        
        # North Node
        if "North Node" in found_planets:
            north_node = next(p for p in complete_chart.placements if p.planet == "North Node")
            print(f"   ✅ North Node: {north_node.sign} in House {north_node.house} at {north_node.degree:.1f}°")
        else:
            print("   ❌ North Node: MISSING")
        
        # South Node
        if "South Node" in found_planets:
            south_node = next(p for p in complete_chart.placements if p.planet == "South Node")
            print(f"   ✅ South Node: {south_node.sign} in House {south_node.house} at {south_node.degree:.1f}°")
        else:
            print("   ❌ South Node: MISSING")
        
        # Complete list verification
        required_points = [
            "Sun", "Moon", "Mercury", "Venus", "Mars", 
            "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron",
            "North Node", "South Node"
        ]
        
        print(f"\n📊 COMPLETE VERIFICATION:")
        all_present = True
        for point in required_points:
            if point in found_planets:
                print(f"   ✅ {point}")
            else:
                print(f"   ❌ {point}")
                all_present = False
        
        print(f"\n🎯 TOTAL POINTS: {len(found_planets)}/13")
        print(f"🎯 STATUS: {'✅ ALL COMPLETE' if all_present else '❌ MISSING POINTS'}")
        
        # Show sample with nodes
        nodes_data = [p for p in complete_chart.placements if "Node" in p.planet]
        if nodes_data:
            print(f"\n📝 LUNAR NODES JSON:")
            print(json.dumps([{
                "planet": p.planet,
                "sign": p.sign,
                "house": p.house,
                "degree": p.degree,
                "retrograde": p.retrograde
            } for p in nodes_data], indent=2))
        
        return all_present
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def main():
    """Run the lunar nodes verification."""
    success = await test_lunar_nodes()
    
    print(f"\n" + "=" * 50)
    if success:
        print("✅ LUNAR NODES SUCCESSFULLY INCLUDED")
        print("✅ All 13 astrological points present")
    else:
        print("❌ Some points missing - check output above")

if __name__ == "__main__":
    asyncio.run(main())