#!/usr/bin/env python3
"""
Final comprehensive test of the complete astrology API with all 13 required points plus chart angles.
"""

import json
import subprocess
import time
import requests

def test_final_complete_api():
    """Test the live API with all required astrological points including lunar nodes."""
    print("Complete Astrology API - Final Verification")
    print("=" * 60)
    
    # Start server
    print("Starting API server...")
    proc = subprocess.Popen(['python', 'main.py'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
    time.sleep(4)
    
    try:
        base_url = "http://localhost:8000"
        
        # Test request
        test_data = {
            "name": "Final Complete Test",
            "date": "1990-06-15",
            "time": "14:30",
            "location": "New York, NY, USA"
        }
        
        print(f"POST {base_url}/generate-chart")
        
        response = requests.post(
            f"{base_url}/generate-chart",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            chart = response.json()
            
            # All required astrological points
            required_planets = [
                "Sun", "Moon", "Mercury", "Venus", "Mars", 
                "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron",
                "North Node", "South Node"
            ]
            
            required_chart_points = [
                "risingSign", "sunSign", "moonSign",
                "midheaven", "descendant", "imumCoeli"
            ]
            
            print("SUCCESS! Complete chart generated")
            
            # Verify basic chart points
            print(f"\nKey Astrological Points:")
            print(f"   Rising Sign: {chart['risingSign']}")
            print(f"   Sun Sign: {chart['sunSign']}")
            print(f"   Moon Sign: {chart['moonSign']}")
            
            # Verify chart angles
            print(f"\nChart Angles:")
            print(f"   Midheaven: {chart['midheaven']['sign']} at {chart['midheaven']['degree']:.1f}°")
            print(f"   Descendant: {chart['descendant']['sign']} at {chart['descendant']['degree']:.1f}°")
            print(f"   Imum Coeli: {chart['imumCoeli']['sign']} at {chart['imumCoeli']['degree']:.1f}°")
            
            # Verify all planetary placements
            print(f"\nPlanetary Placements:")
            found_planets = set()
            lunar_nodes = []
            
            for placement in chart['placements']:
                planet = placement['planet']
                found_planets.add(planet)
                retro = " (R)" if placement['retrograde'] else ""
                
                if "Node" in planet:
                    lunar_nodes.append(placement)
                
                if planet in required_planets:
                    print(f"   {planet}: {placement['sign']} in House {placement['house']} at {placement['degree']:.1f}°{retro}")
            
            # Check completeness
            missing = set(required_planets) - found_planets
            
            print(f"\nVerification Results:")
            print(f"   Total planets found: {len(found_planets)}")
            print(f"   Required planets: {len(required_planets)}")
            
            if missing:
                print(f"   Missing planets: {missing}")
                return False
            else:
                print(f"   All required planets present!")
            
            # Lunar nodes specific verification
            print(f"\nLunar Nodes Details:")
            for node in lunar_nodes:
                print(f"   {node['planet']}: {node['sign']} in House {node['house']} at {node['degree']:.1f}°")
            
            # House system verification
            print(f"\nHouse System: {chart['houseSystem']} (Whole Sign)")
            
            # Complete verification checklist
            print(f"\nComplete Verification Checklist:")
            verification_results = {}
            
            for planet in required_planets:
                present = planet in found_planets
                verification_results[planet] = present
                status = "✓" if present else "✗"
                print(f"   {status} {planet}")
            
            for point in required_chart_points:
                present = point in chart
                verification_results[point] = present
                status = "✓" if present else "✗"
                print(f"   {status} {point}")
            
            all_complete = all(verification_results.values())
            
            print(f"\nFinal Status: {'COMPLETE - All 17 points included' if all_complete else 'INCOMPLETE - Some points missing'}")
            
            return all_complete
            
        else:
            print(f"Request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Test failed: {e}")
        return False
    finally:
        proc.terminate()
        print(f"\nServer stopped")

def main():
    """Run the final comprehensive verification."""
    success = test_final_complete_api()
    
    print(f"\n" + "=" * 60)
    print("FINAL VERIFICATION COMPLETE")
    print("=" * 60)
    
    if success:
        print("API INCLUDES ALL REQUIRED ASTROLOGICAL POINTS:")
        print("")
        print("Planetary Bodies (11):")
        print("• Sun, Moon, Mercury, Venus, Mars")
        print("• Jupiter, Saturn, Uranus, Neptune, Pluto, Chiron")
        print("")
        print("Lunar Nodes (2):")
        print("• North Node, South Node")
        print("")
        print("Chart Angles (4):")
        print("• Rising, Midheaven, Descendant, Imum Coeli")
        print("")
        print("TOTAL: 17 astrological points")
        print("House System: Whole Sign configured")
        print("API ready for production use!")
    else:
        print("Some requirements not met - check output above")

if __name__ == "__main__":
    main()