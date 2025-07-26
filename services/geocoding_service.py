"""
Geocoding service for converting location names to coordinates.

This service uses the OpenStreetMap Nominatim API to convert location names
into latitude/longitude coordinates with timezone estimation.
"""

import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class GeocodingService:
    """Service for geocoding location names to coordinates."""
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.timeout = 10
    
    async def get_coordinates(self, location: str) -> Dict[str, Any]:
        """
        Get coordinates and timezone for a location name.
        
        Args:
            location: Location name (e.g., "New York, NY, USA")
            
        Returns:
            Dictionary with latitude, longitude, timezone, and display_name
            
        Raises:
            Exception: If geocoding fails
        """
        try:
            logger.info(f"Geocoding location: {location}")
            
            # Make request to Nominatim API
            response = requests.get(
                f"{self.base_url}/search",
                params={
                    "format": "json",
                    "q": location,
                    "limit": 1,
                    "addressdetails": 1
                },
                timeout=self.timeout,
                headers={
                    "User-Agent": "Astrology-Chart-API/1.0 (contact@example.com)"
                }
            )
            
            if not response.ok:
                raise Exception(f"Geocoding request failed with status {response.status_code}")
            
            data = response.json()
            
            if not data or len(data) == 0:
                raise Exception(f"Location '{location}' not found")
            
            result = data[0]
            latitude = float(result["lat"])
            longitude = float(result["lon"])
            
            # Estimate timezone based on longitude (rough approximation)
            # This is a simple estimation: UTC offset = longitude / 15
            timezone = round(longitude / 15)
            
            logger.info(f"Successfully geocoded '{location}' to {latitude}, {longitude}")
            
            return {
                "location": location,
                "latitude": latitude,
                "longitude": longitude,
                "timezone": timezone,
                "display_name": result.get("display_name", location)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Geocoding request failed: {str(e)}")
            raise Exception(f"Failed to geocode location: {str(e)}")
        except (ValueError, KeyError) as e:
            logger.error(f"Invalid geocoding response: {str(e)}")
            raise Exception(f"Invalid response from geocoding service: {str(e)}")
        except Exception as e:
            logger.error(f"Geocoding error: {str(e)}")
            raise Exception(f"Geocoding failed: {str(e)}")
    
    def estimate_timezone_from_longitude(self, longitude: float) -> float:
        """
        Estimate timezone offset from longitude.
        
        This is a rough approximation and may not be accurate for all locations.
        For production use, consider using a proper timezone API.
        
        Args:
            longitude: Longitude coordinate
            
        Returns:
            Estimated timezone offset in hours
        """
        return round(longitude / 15)