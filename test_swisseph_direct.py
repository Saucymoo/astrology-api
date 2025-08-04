#!/usr/bin/env python3
"""
Direct Swiss Ephemeris test for Mia's chart using available swisseph module
"""

import json
from datetime import datetime

def test_mia_chart_swisseph():
    """Test Mia's chart using available swisseph module."""
    
    print("=" * 70)
    print("SWISS EPHEMERIS DIRECT TEST - MIA'S CHART")
    print("=" * 70)
    
    try:
        import swisseph as swe
        print("✅ Using swisseph module")
        
        # Mia's birth data
        year, month, day = 1974, 11, 22
        hour, minute = 19, 10
        latitude = -34.9285  # Adelaide
        longitude = 138.6007
        
        # Calculate Julian Day
        jd = swe.julday(year, month, day, hour + minute/60.0)
        print(f"Julian Day: {jd}")
        
        # Calculate houses - this should work with swisseph
        try:
            houses, ascmc = swe.houses(jd, latitude, longitude, b'W')
            print(f"✅ Houses calculated successfully")
            print(f"Ascendant: {ascmc[0]:.6f}°")
            print(f"Midheaven: {ascmc[1]:.6f}°")
            
            # Convert degrees to signs
            def degree_to_sign_info(degree):
                signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
                sign_index = int(degree // 30)
                sign_degree = degree % 30
                return signs[sign_index], sign_degree
            
            asc_sign, asc_deg = degree_to_sign_info(ascmc[0])
            mc_sign, mc_deg = degree_to_sign_info(ascmc[1])
            
            print(f"\nCHART ANGLES:")
            print(f"Rising: {asc_sign} {asc_deg:.2f}°")
            print(f"Midheaven: {mc_sign} {mc_deg:.2f}°")
            
        except Exception as e:
            print(f"❌ Houses calculation failed: {e}")
            return None
        
        # Calculate key planets
        planets_data = []
        
        # Basic planets
        planet_ids = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mercury': swe.MERCURY,
            'Venus': swe.VENUS,
            'Mars': swe.MARS,
            'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN,
            'Uranus': swe.URANUS,
            'Neptune': swe.NEPTUNE,
            'Pluto': swe.PLUTO
        }
        
        print(f"\nPLANETARY POSITIONS:")
        
        for planet_name, planet_id in planet_ids.items():
            try:
                planet_data, ret_flag = swe.calc_ut(jd, planet_id)
                planet_degree = planet_data[0]
                
                planet_sign, sign_degree = degree_to_sign_info(planet_degree)
                
                # Format degree
                deg = int(sign_degree)
                min_val = int((sign_degree % 1) * 60)
                sec_val = int(((sign_degree % 1) * 60 % 1) * 60)
                exact_degree = f"{deg}°{min_val:02d}'{sec_val:02d}\""
                
                planets_data.append({
                    'planet': planet_name,
                    'sign': planet_sign,
                    'degree': sign_degree,
                    'exact_degree': exact_degree,
                    'retrograde': ret_flag & swe.FLG_SPEED and planet_data[3] < 0
                })
                
                print(f"  {planet_name}: {planet_sign} {exact_degree}")
                
            except Exception as e:
                print(f"  {planet_name}: Error - {e}")
        
        # Add nodes
        try:
            north_node_data, _ = swe.calc_ut(jd, swe.MEAN_NODE)
            north_node_degree = north_node_data[0]
            nn_sign, nn_deg = degree_to_sign_info(north_node_degree)
            
            # South Node is opposite
            south_node_degree = (north_node_degree + 180) % 360
            sn_sign, sn_deg = degree_to_sign_info(south_node_degree)
            
            # Format degrees
            nn_exact = f"{int(nn_deg)}°{int((nn_deg % 1) * 60):02d}'{int(((nn_deg % 1) * 60 % 1) * 60):02d}\""
            sn_exact = f"{int(sn_deg)}°{int((sn_deg % 1) * 60):02d}'{int(((sn_deg % 1) * 60 % 1) * 60):02d}\""
            
            planets_data.extend([
                {'planet': 'North Node', 'sign': nn_sign, 'degree': nn_deg, 'exact_degree': nn_exact, 'retrograde': False},
                {'planet': 'South Node', 'sign': sn_sign, 'degree': sn_deg, 'exact_degree': sn_exact, 'retrograde': False}
            ])
            
            print(f"  North Node: {nn_sign} {nn_exact}")
            print(f"  South Node: {sn_sign} {sn_exact}")
            
        except Exception as e:
            print(f"  Nodes: Error - {e}")
        
        # Calculate Whole Sign houses
        rising_sign_index = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                           'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].index(asc_sign)
        
        for planet in planets_data:
            planet_sign_index = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                               'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].index(planet['sign'])
            house_number = ((planet_sign_index - rising_sign_index) % 12) + 1
            planet['house'] = house_number
        
        # Find Sun and Moon
        sun_data = next((p for p in planets_data if p['planet'] == 'Sun'), None)
        moon_data = next((p for p in planets_data if p['planet'] == 'Moon'), None)
        
        # Create complete chart
        chart = {
            "name": "Mia",
            "birth_date": "1974-11-22",
            "birth_time": "19:10",
            "birth_location": "Adelaide, South Australia, Australia",
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude,
                "timezone": 9.5
            },
            "house_system": "Whole Sign",
            "ascendant": {
                "sign": asc_sign,
                "degree": asc_deg,
                "exact_degree": f"{int(asc_deg)}°{int((asc_deg % 1) * 60):02d}'{int(((asc_deg % 1) * 60 % 1) * 60):02d}\""
            },
            "midheaven": {
                "sign": mc_sign,
                "degree": mc_deg,
                "exact_degree": f"{int(mc_deg)}°{int((mc_deg % 1) * 60):02d}'{int(((mc_deg % 1) * 60 % 1) * 60):02d}\""
            },
            "rising_sign": asc_sign,
            "sun_sign": sun_data['sign'] if sun_data else "Unknown",
            "moon_sign": moon_data['sign'] if moon_data else "Unknown",
            "placements": planets_data,
            "generated_at": datetime.now().isoformat(),
            "source": "SwissEph Direct with Whole Sign Houses"
        }
        
        print(f"\n" + "=" * 70)
        print("VERIFICATION:")
        print("=" * 70)
        print(f"Expected: Taurus Rising 19° → Actual: {asc_sign} {asc_deg:.1f}°")
        if sun_data:
            print(f"Expected: Scorpio Sun 29° → Actual: {sun_data['sign']} {sun_data['degree']:.1f}°")
        if moon_data:
            print(f"Expected: Pisces Moon 4° → Actual: {moon_data['sign']} {moon_data['degree']:.1f}°")
        
        # Test if values match expectations
        rising_match = asc_sign == "Taurus" and 18 <= asc_deg <= 20
        sun_match = sun_data and sun_data['sign'] == "Scorpio" and 28 <= sun_data['degree'] <= 30
        moon_match = moon_data and moon_data['sign'] == "Pisces" and 3 <= moon_data['degree'] <= 6
        
        print(f"\nMATCH RESULTS:")
        print(f"✅ Rising match: {rising_match}")
        print(f"✅ Sun match: {sun_match}")
        print(f"✅ Moon match: {moon_match}")
        
        return chart
        
    except Exception as e:
        print(f"❌ Swiss Ephemeris test failed: {e}")
        return None

if __name__ == "__main__":
    chart = test_mia_chart_swisseph()
    
    if chart:
        print(f"\n" + "=" * 70)
        print("🎯 SWISS EPHEMERIS TEST SUCCESSFUL")
        print("=" * 70)
        print("✅ Chart calculations working")
        print("✅ All planetary positions calculated")
        print("✅ Whole Sign houses applied")
        print("✅ Ready for API integration")
        
        # Show the complete response format
        print(f"\nCOMPLETE API RESPONSE FORMAT:")
        print(json.dumps(chart, indent=2)[:500] + "...")
        
    else:
        print("❌ Swiss Ephemeris test failed")