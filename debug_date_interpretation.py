#!/usr/bin/env python3
"""
Debug the date interpretation to ensure November 22, 1974 produces correct Sun sign.
"""

from datetime import datetime
from models import BirthInfoRequest

def test_date_parsing():
    """Test how dates are being parsed and validated."""
    
    print("DEBUGGING DATE INTERPRETATION")
    print("=" * 50)
    
    # Test the date validator
    test_dates = [
        "22/11/1974",  # DD/MM/YYYY - should be November 22, 1974
        "1974-11-22",  # ISO format - November 22, 1974
    ]
    
    for date_str in test_dates:
        print(f"\nTesting date: {date_str}")
        try:
            # Create a birth info request to test validation
            birth_request = BirthInfoRequest(
                name="Test",
                date=date_str,
                time="19:10",
                location="Adelaide, Australia"
            )
            
            validated_date = birth_request.date
            print(f"  Validated as: {validated_date}")
            
            # Parse the validated date to check month/day
            parsed = datetime.strptime(validated_date, '%Y-%m-%d')
            print(f"  Parsed as: {parsed.strftime('%B %d, %Y')}")
            
            # Check expected Sun sign for November 22
            if parsed.month == 11 and parsed.day == 22:
                print(f"  Expected Sun sign: Sagittarius (Sun enters Sagittarius ~Nov 22)")
            else:
                print(f"  WARNING: Date not November 22nd! Month={parsed.month}, Day={parsed.day}")
                
        except Exception as e:
            print(f"  ERROR: {e}")

def check_sun_sign_logic():
    """Check what Sun sign should be for November 22, 1974."""
    
    print("\n" + "=" * 50)
    print("SUN SIGN VERIFICATION")
    print("=" * 50)
    
    # Sun sign dates (approximate)
    sun_signs = [
        ("Sagittarius", "Nov 22 - Dec 21"),
        ("Scorpio", "Oct 23 - Nov 21"),
        ("Libra", "Sep 23 - Oct 22"),
    ]
    
    print("Sun sign seasons:")
    for sign, dates in sun_signs:
        print(f"  {sign}: {dates}")
    
    print(f"\nNovember 22, 1974 should be: SAGITTARIUS")
    print(f"(Sun enters Sagittarius around November 22nd)")

if __name__ == "__main__":
    test_date_parsing()
    check_sun_sign_logic()