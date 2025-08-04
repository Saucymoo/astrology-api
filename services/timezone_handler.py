"""
Comprehensive timezone handling for accurate birth chart calculations worldwide.
Handles historical timezone rules, daylight saving transitions, and coordinate-based timezone detection.
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Tuple, Optional, Dict, Any
import math
import requests

logger = logging.getLogger(__name__)

class TimezoneHandler:
    """
    Handles timezone calculations for accurate astrological chart generation.
    Supports historical timezone rules and daylight saving time transitions.
    """
    
    def __init__(self):
        # Major timezone regions with historical DST rules
        self.timezone_regions = {
            # Australia
            'adelaide': {'standard_offset': 9.5, 'dst_months': [10, 11, 12, 1, 2, 3], 'dst_offset': 10.5},
            'sydney': {'standard_offset': 10.0, 'dst_months': [10, 11, 12, 1, 2, 3], 'dst_offset': 11.0},
            'melbourne': {'standard_offset': 10.0, 'dst_months': [10, 11, 12, 1, 2, 3], 'dst_offset': 11.0},
            'perth': {'standard_offset': 8.0, 'dst_months': [], 'dst_offset': 8.0},
            'darwin': {'standard_offset': 9.5, 'dst_months': [], 'dst_offset': 9.5},
            
            # North America
            'new_york': {'standard_offset': -5.0, 'dst_months': [3, 4, 5, 6, 7, 8, 9, 10], 'dst_offset': -4.0},
            'los_angeles': {'standard_offset': -8.0, 'dst_months': [3, 4, 5, 6, 7, 8, 9, 10], 'dst_offset': -7.0},
            'chicago': {'standard_offset': -6.0, 'dst_months': [3, 4, 5, 6, 7, 8, 9, 10], 'dst_offset': -5.0},
            'denver': {'standard_offset': -7.0, 'dst_months': [3, 4, 5, 6, 7, 8, 9, 10], 'dst_offset': -6.0},
            
            # Europe
            'london': {'standard_offset': 0.0, 'dst_months': [3, 4, 5, 6, 7, 8, 9, 10], 'dst_offset': 1.0},
            'paris': {'standard_offset': 1.0, 'dst_months': [3, 4, 5, 6, 7, 8, 9, 10], 'dst_offset': 2.0},
            'berlin': {'standard_offset': 1.0, 'dst_months': [3, 4, 5, 6, 7, 8, 9, 10], 'dst_offset': 2.0},
            'moscow': {'standard_offset': 3.0, 'dst_months': [], 'dst_offset': 3.0},
            
            # Asia
            'tokyo': {'standard_offset': 9.0, 'dst_months': [], 'dst_offset': 9.0},
            'beijing': {'standard_offset': 8.0, 'dst_months': [], 'dst_offset': 8.0},
            'mumbai': {'standard_offset': 5.5, 'dst_months': [], 'dst_offset': 5.5},
            'dubai': {'standard_offset': 4.0, 'dst_months': [], 'dst_offset': 4.0},
        }
        
        # Historical timezone introduction dates
        self.dst_history = {
            'australia': {
                'adelaide': {'introduced': 1971, 'start_month': 10, 'end_month': 3},
                'sydney': {'introduced': 1971, 'start_month': 10, 'end_month': 3},
                'melbourne': {'introduced': 1971, 'start_month': 10, 'end_month': 3},
            },
            'usa': {
                'introduced': 1918, 'modern_rules': 2007,
                'start_month': 3, 'end_month': 11
            },
            'europe': {
                'introduced': 1980, 'start_month': 3, 'end_month': 10
            }
        }

    def calculate_accurate_utc_time(self, 
                                   birth_date: str, 
                                   birth_time: str,
                                   latitude: float, 
                                   longitude: float,
                                   location_name: str = "") -> Tuple[float, Dict[str, Any]]:
        """
        Calculate accurate UTC time considering historical timezone rules.
        
        Args:
            birth_date: Date in YYYY-MM-DD format
            birth_time: Time in HH:MM format (24-hour)
            latitude: Latitude coordinate
            longitude: Longitude coordinate  
            location_name: Location name for timezone lookup
            
        Returns:
            Tuple of (decimal_utc_time, timezone_info)
        """
        try:
            # Parse date and time
            year = int(birth_date.split('-')[0])
            month = int(birth_date.split('-')[1])
            day = int(birth_date.split('-')[2])
            hour = int(birth_time.split(':')[0])
            minute = int(birth_time.split(':')[1])
            
            decimal_local_time = hour + minute / 60.0
            
            # Determine timezone offset
            timezone_offset, timezone_info = self._determine_timezone_offset(
                year, month, latitude, longitude, location_name
            )
            
            # Convert to UTC
            decimal_utc_time = decimal_local_time - timezone_offset
            
            # Handle day rollover
            utc_day = day
            if decimal_utc_time < 0:
                decimal_utc_time += 24
                utc_day -= 1
            elif decimal_utc_time >= 24:
                decimal_utc_time -= 24
                utc_day += 1
            
            timezone_info.update({
                'original_day': day,
                'utc_day': utc_day,
                'local_time': f"{hour:02d}:{minute:02d}",
                'utc_time': f"{int(decimal_utc_time):02d}:{int((decimal_utc_time % 1) * 60):02d}",
                'timezone_offset': timezone_offset
            })
            
            logger.info(f"Timezone calculation: {location_name} {year}-{month:02d} "
                       f"Local {hour:02d}:{minute:02d} = UTC {decimal_utc_time:.2f} "
                       f"(offset {timezone_offset:+.1f}h)")
            
            return decimal_utc_time, timezone_info
            
        except Exception as e:
            logger.error(f"UTC time calculation failed: {e}")
            raise Exception(f"Failed to calculate UTC time: {str(e)}")

    def _determine_timezone_offset(self, 
                                  year: int, 
                                  month: int,
                                  latitude: float, 
                                  longitude: float,
                                  location_name: str) -> Tuple[float, Dict[str, Any]]:
        """
        Determine timezone offset for given location and date.
        
        Returns:
            Tuple of (offset_hours, timezone_info_dict)
        """
        
        # Try specific location lookup first
        location_key = self._normalize_location_name(location_name)
        if location_key in self.timezone_regions:
            return self._get_historical_offset(location_key, year, month)
        
        # Try coordinate-based timezone detection
        try:
            coordinate_offset = self._get_timezone_from_coordinates(
                latitude, longitude, year, month
            )
            if coordinate_offset is not None:
                return coordinate_offset
        except Exception as e:
            logger.warning(f"Coordinate timezone lookup failed: {e}")
        
        # Fallback to approximate longitude-based calculation
        return self._approximate_timezone_from_longitude(longitude, year, month)

    def _normalize_location_name(self, location_name: str) -> str:
        """Normalize location name for timezone lookup."""
        if not location_name:
            return ""
        
        location_lower = location_name.lower()
        
        # City name mapping
        city_mappings = {
            'adelaide': 'adelaide',
            'sydney': 'sydney', 
            'melbourne': 'melbourne',
            'perth': 'perth',
            'darwin': 'darwin',
            'new york': 'new_york',
            'los angeles': 'los_angeles',
            'chicago': 'chicago',
            'denver': 'denver',
            'london': 'london',
            'paris': 'paris',
            'berlin': 'berlin',
            'moscow': 'moscow',
            'tokyo': 'tokyo',
            'beijing': 'beijing',
            'mumbai': 'mumbai',
            'dubai': 'dubai'
        }
        
        for city_variant, city_key in city_mappings.items():
            if city_variant in location_lower:
                return city_key
        
        # State/region mappings
        if 'south australia' in location_lower or 'sa' in location_lower:
            return 'adelaide'
        elif 'new south wales' in location_lower or 'nsw' in location_lower:
            return 'sydney'
        elif 'victoria' in location_lower:
            return 'melbourne'
        elif 'western australia' in location_lower or 'wa' in location_lower:
            return 'perth'
        
        return ""

    def _get_historical_offset(self, 
                              location_key: str, 
                              year: int, 
                              month: int) -> Tuple[float, Dict[str, Any]]:
        """Get historical timezone offset for specific location."""
        
        region_info = self.timezone_regions[location_key]
        standard_offset = region_info['standard_offset']
        dst_offset = region_info['dst_offset']
        dst_months = region_info['dst_months']
        
        # Check if DST was in use for this year
        dst_active = False
        dst_info = {"dst_introduced": "Unknown", "dst_active": False}
        
        # Australia specific rules
        if location_key in ['adelaide', 'sydney', 'melbourne']:
            if year >= 1971:  # DST introduced in 1971
                dst_active = month in dst_months
                dst_info = {
                    "dst_introduced": 1971,
                    "dst_active": dst_active,
                    "dst_rule": "October to March"
                }
        
        # USA specific rules  
        elif location_key in ['new_york', 'los_angeles', 'chicago', 'denver']:
            if year >= 1918:  # DST introduced during WWI
                dst_active = month in dst_months
                dst_info = {
                    "dst_introduced": 1918,
                    "dst_active": dst_active,
                    "dst_rule": "March to November (modern)"
                }
        
        # Europe specific rules
        elif location_key in ['london', 'paris', 'berlin']:
            if year >= 1980:  # Modern EU DST rules
                dst_active = month in dst_months
                dst_info = {
                    "dst_introduced": 1980,
                    "dst_active": dst_active,
                    "dst_rule": "March to October"
                }
        
        offset = dst_offset if dst_active else standard_offset
        
        timezone_info = {
            "location": location_key,
            "method": "historical_lookup",
            "standard_offset": standard_offset,
            "dst_offset": dst_offset,
            "final_offset": offset,
            **dst_info
        }
        
        return offset, timezone_info

    def _get_timezone_from_coordinates(self, 
                                     latitude: float, 
                                     longitude: float,
                                     year: int, 
                                     month: int) -> Optional[Tuple[float, Dict[str, Any]]]:
        """
        Get timezone from coordinates using online timezone API.
        Note: This requires internet connection and may not have historical data.
        """
        try:
            # Use a free timezone API (TimeZoneDB, WorldTimeAPI, etc.)
            # This is a simplified implementation - in production you'd use a proper API
            
            # Approximate timezone from longitude as fallback
            approximate_offset = longitude / 15.0  # Rough calculation
            
            # Round to nearest 0.5 hour (common timezone increments)
            rounded_offset = round(approximate_offset * 2) / 2
            
            timezone_info = {
                "method": "coordinate_approximation",
                "longitude": longitude,
                "latitude": latitude,
                "approximate_offset": approximate_offset,
                "rounded_offset": rounded_offset,
                "note": "Approximate calculation - may not account for DST"
            }
            
            return rounded_offset, timezone_info
            
        except Exception as e:
            logger.warning(f"Coordinate timezone lookup failed: {e}")
            return None

    def _approximate_timezone_from_longitude(self, 
                                           longitude: float,
                                           year: int, 
                                           month: int) -> Tuple[float, Dict[str, Any]]:
        """
        Fallback method: approximate timezone from longitude.
        This is the least accurate method but always works.
        """
        
        # Basic longitude to timezone conversion
        approximate_offset = longitude / 15.0
        
        # Round to nearest 0.5 hour
        rounded_offset = round(approximate_offset * 2) / 2
        
        timezone_info = {
            "method": "longitude_approximation",
            "longitude": longitude,
            "approximate_offset": approximate_offset,
            "rounded_offset": rounded_offset,
            "warning": "Fallback method - may be inaccurate",
            "note": "Does not account for political timezone boundaries or DST"
        }
        
        logger.warning(f"Using longitude approximation for timezone: {rounded_offset:+.1f}h")
        
        return rounded_offset, timezone_info

    def get_timezone_info_summary(self, timezone_info: Dict[str, Any]) -> str:
        """Generate human-readable timezone information summary."""
        
        method = timezone_info.get('method', 'unknown')
        offset = timezone_info.get('final_offset', timezone_info.get('rounded_offset', 0))
        
        summary = f"Timezone: UTC{offset:+.1f}"
        
        if method == 'historical_lookup':
            location = timezone_info.get('location', 'unknown')
            dst_active = timezone_info.get('dst_active', False)
            summary += f" ({location}, {'DST active' if dst_active else 'Standard time'})"
        elif method == 'coordinate_approximation':
            summary += " (coordinate-based approximation)"
        elif method == 'longitude_approximation':
            summary += " (longitude approximation - less accurate)"
        
        return summary

# Global instance
timezone_handler = TimezoneHandler()