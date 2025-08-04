#!/usr/bin/env python3
"""
Comprehensive accuracy test suite for verifying chart calculations
Compare against known accurate sources and famous birth charts
"""

import requests
import json
from datetime import datetime

def test_famous_birth_charts():
    """Test with famous people's publicly known birth data for accuracy verification."""
    
    print("FAMOUS BIRTH CHARTS ACCURACY TEST")
    print("="*70)
    print("Comparing against publicly documented birth data")
    print()
    
    # Famous charts with well-documented birth data
    famous_charts = [
        {
            "name": "Albert Einstein",
            "birth_date": "1879-03-14",
            "birth_time": "11:30",
            "birth_location": "Ulm, Germany",
            "expected": {
                "sun": "Pisces",  # March 14 = Pisces
                "description": "Genius physicist, intuitive Pisces"
            }
        },
        {
            "name": "Winston Churchill", 
            "birth_date": "1874-11-30",
            "birth_time": "01:30",
            "birth_location": "Woodstock, UK",
            "expected": {
                "sun": "Sagittarius",  # November 30 = Sagittarius
                "description": "British PM, Sagittarian leadership"
            }
        },
        {
            "name": "John F. Kennedy",
            "birth_date": "1917-05-29", 
            "birth_time": "15:00",
            "birth_location": "Brookline, MA, USA",
            "expected": {
                "sun": "Gemini",  # May 29 = Gemini
                "description": "US President, Gemini communicator"
            }
        },
        {
            "name": "Princess Diana",
            "birth_date": "1961-07-01",
            "birth_time": "19:45", 
            "birth_location": "Sandringham, UK",
            "expected": {
                "sun": "Cancer",  # July 1 = Cancer
                "description": "Royal, nurturing Cancer"
            }
        }
    ]
    
    results = []
    
    for i, chart_data in enumerate(famous_charts, 1):
        print(f"TEST {i}: {chart_data['name']}")
        print(f"Birth: {chart_data['birth_date']} at {chart_data['birth_time']}")
        print(f"Location: {chart_data['birth_location']}")
        print(f"Expected: {chart_data['expected']['sun']} Sun")
        print(f"Context: {chart_data['expected']['description']}")
        
        try:
            response = requests.post(
                "http://localhost:8000/generate-chart",
                json={
                    "name": chart_data["name"],
                    "birth_date": chart_data["birth_date"],
                    "birth_time": chart_data["birth_time"], 
                    "birth_location": chart_data["birth_location"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                chart = response.json()
                sun_sign = chart['sun_sign']
                rising_sign = chart['rising_sign']
                moon_sign = chart['moon_sign']
                
                # Get detailed sun position
                sun_data = next(p for p in chart['placements'] if p['planet'] == 'Sun')
                
                sun_correct = sun_sign == chart_data['expected']['sun']
                
                print(f"RESULT:")
                print(f"  Sun: {sun_sign} {sun_data['exact_degree']} {'✅' if sun_correct else '❌'}")
                print(f"  Moon: {moon_sign}")
                print(f"  Rising: {rising_sign} {chart['ascendant']['exact_degree']}")
                print(f"  Coordinates: {chart['coordinates']['latitude']:.2f}°, {chart['coordinates']['longitude']:.2f}°")
                
                results.append({
                    'name': chart_data['name'],
                    'expected_sun': chart_data['expected']['sun'],
                    'actual_sun': sun_sign,
                    'correct': sun_correct,
                    'full_chart': chart
                })
                
                print(f"  Status: {'✅ ACCURATE' if sun_correct else '❌ INACCURATE'}")
                
            else:
                print(f"  ❌ API Error: {response.status_code}")
                results.append({
                    'name': chart_data['name'],
                    'error': f"API Error {response.status_code}"
                })
                
        except Exception as e:
            print(f"  ❌ Test Error: {e}")
            results.append({
                'name': chart_data['name'],
                'error': str(e)
            })
        
        print("-" * 70)
    
    # Summary
    successful_tests = [r for r in results if 'correct' in r and r['correct']]
    total_tests = len([r for r in results if 'correct' in r])
    
    print(f"\nACCURACY SUMMARY:")
    print(f"Successful sun sign matches: {len(successful_tests)}/{total_tests}")
    print(f"Accuracy rate: {len(successful_tests)/total_tests*100:.1f}%" if total_tests > 0 else "No valid tests")
    
    return results

def test_seasonal_accuracy():
    """Test charts at key seasonal points to verify sun sign accuracy."""
    
    print("\n" + "="*70)
    print("SEASONAL ACCURACY TEST")
    print("="*70)
    print("Testing sun positions at equinoxes and solstices")
    print()
    
    seasonal_tests = [
        {
            "name": "Spring Equinox Test",
            "birth_date": "1990-03-21",  # Spring equinox
            "birth_time": "12:00",
            "birth_location": "London, UK",
            "expected_sun": "Aries",
            "description": "Should be at 0° Aries (start of zodiac)"
        },
        {
            "name": "Summer Solstice Test", 
            "birth_date": "1990-06-21",  # Summer solstice
            "birth_time": "12:00",
            "birth_location": "New York, NY, USA",
            "expected_sun": "Gemini",  # Usually late Gemini
            "description": "Longest day, late Gemini/early Cancer"
        },
        {
            "name": "Autumn Equinox Test",
            "birth_date": "1990-09-23",  # Autumn equinox
            "birth_time": "12:00", 
            "birth_location": "Sydney, Australia",
            "expected_sun": "Libra",
            "description": "Should be at 0° Libra (balance point)"
        },
        {
            "name": "Winter Solstice Test",
            "birth_date": "1990-12-21",  # Winter solstice
            "birth_time": "12:00",
            "birth_location": "Berlin, Germany", 
            "expected_sun": "Sagittarius",  # Usually late Sagittarius
            "description": "Shortest day, late Sagittarius/early Capricorn"
        }
    ]
    
    seasonal_results = []
    
    for test_data in seasonal_tests:
        print(f"{test_data['name']}: {test_data['birth_date']}")
        print(f"Expected: {test_data['expected_sun']} - {test_data['description']}")
        
        try:
            response = requests.post(
                "http://localhost:8000/generate-chart",
                json={
                    "name": test_data["name"],
                    "birth_date": test_data["birth_date"],
                    "birth_time": test_data["birth_time"],
                    "birth_location": test_data["birth_location"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                chart = response.json()
                sun_data = next(p for p in chart['placements'] if p['planet'] == 'Sun')
                
                sun_correct = chart['sun_sign'] == test_data['expected_sun']
                print(f"Result: {chart['sun_sign']} {sun_data['exact_degree']} {'✅' if sun_correct else '❌'}")
                
                seasonal_results.append({
                    'test': test_data['name'],
                    'expected': test_data['expected_sun'],
                    'actual': chart['sun_sign'],
                    'correct': sun_correct
                })
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    return seasonal_results

def compare_with_online_calculator():
    """Instructions for comparing with online astrology calculators."""
    
    print("\n" + "="*70)
    print("ONLINE CALCULATOR VERIFICATION GUIDE")
    print("="*70)
    print()
    print("To verify accuracy against established sources:")
    print()
    print("1. ASTRO.COM (Most Accurate)")
    print("   URL: https://www.astro.com/horoscopes/chart-drawing")
    print("   - Use Extended Chart Selection")
    print("   - Select 'Whole Sign Houses' system")
    print("   - Enter Mia's data: Nov 22, 1974, 7:10 PM, Adelaide")
    print("   - Compare planetary positions degree by degree")
    print()
    print("2. ASTRO-CHARTS.COM")
    print("   URL: https://astro-charts.com/tools/new-chart/")
    print("   - Professional-grade calculations")
    print("   - Shows exact degrees and minutes")
    print("   - Supports Whole Sign houses")
    print()
    print("3. ASTROTHEME.COM")
    print("   URL: https://www.astrotheme.com/horoscope_chart_sign_ascendant.php")
    print("   - Celebrity charts for comparison") 
    print("   - Historical birth data database")
    print()
    print("4. CAFEASTROLOGY.COM")
    print("   URL: https://cafeastrology.com/natal-chart-report.html")
    print("   - Free detailed reports")
    print("   - Good for quick verification")
    print()
    print("COMPARISON CHECKLIST:")
    print("□ Sun sign and exact degree")
    print("□ Moon sign and exact degree") 
    print("□ Ascendant/Rising sign and degree")
    print("□ Midheaven sign and degree")
    print("□ All planetary positions")
    print("□ House system (must be Whole Sign)")
    print("□ Coordinate accuracy for Adelaide")

def generate_test_report():
    """Generate a comprehensive test report."""
    
    print("\n" + "="*70)
    print("GENERATING COMPREHENSIVE TEST REPORT")
    print("="*70)
    
    # Run all tests
    famous_results = test_famous_birth_charts()
    seasonal_results = test_seasonal_accuracy()
    
    # Create detailed report
    report = {
        "test_date": datetime.now().isoformat(),
        "famous_charts": famous_results,
        "seasonal_tests": seasonal_results,
        "mia_chart_data": {
            "name": "Mia Mitchell",
            "birth_date": "1974-11-22",
            "birth_time": "19:10",
            "birth_location": "Adelaide, South Australia, Australia"
        }
    }
    
    # Test Mia's chart one more time
    print("\nFINAL MIA CHART VERIFICATION:")
    try:
        response = requests.post(
            "http://localhost:8000/generate-chart",
            json=report["mia_chart_data"],
            timeout=30
        )
        
        if response.status_code == 200:
            mia_chart = response.json()
            report["mia_final_result"] = mia_chart
            
            print(f"Mia's Chart:")
            print(f"  Sun: {mia_chart['sun_sign']}")
            print(f"  Moon: {mia_chart['moon_sign']}")
            print(f"  Rising: {mia_chart['rising_sign']} {mia_chart['ascendant']['exact_degree']}")
            print(f"  House System: {mia_chart['house_system']}")
            
    except Exception as e:
        print(f"Mia chart error: {e}")
        report["mia_error"] = str(e)
    
    # Save report
    with open('accuracy_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Complete test report saved to 'accuracy_test_report.json'")
    print("\nNext steps for verification:")
    print("1. Review the test results above")
    print("2. Compare against online calculators using the guide")
    print("3. Check the saved JSON report for detailed data")
    
    return report

if __name__ == "__main__":
    print("ASTROLOGY API ACCURACY VERIFICATION SUITE")
    print("Testing against known birth data and seasonal markers")
    print()
    
    # Generate comprehensive report
    report = generate_test_report()
    
    # Show online verification guide
    compare_with_online_calculator()
    
    print(f"\n🎯 ACCURACY TESTING COMPLETE")
    print("Use the online calculator guide above to verify against professional sources")