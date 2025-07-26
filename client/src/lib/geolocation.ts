export interface Coordinates {
  latitude: number;
  longitude: number;
  timezone?: number;
}

export interface LocationInfo {
  name: string;
  coordinates: Coordinates;
}

/**
 * Get user's current location using browser geolocation API
 * @returns Promise resolving to coordinates
 */
export function getCurrentLocation(): Promise<Coordinates> {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported by this browser.'));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        // Estimate timezone based on longitude (rough approximation)
        const timezone = Math.round(longitude / 15);
        
        resolve({
          latitude,
          longitude,
          timezone,
        });
      },
      (error) => {
        let message = 'Unable to retrieve your location.';
        
        switch (error.code) {
          case error.PERMISSION_DENIED:
            message = 'Location permission denied by user.';
            break;
          case error.POSITION_UNAVAILABLE:
            message = 'Location information is unavailable.';
            break;
          case error.TIMEOUT:
            message = 'Location request timed out.';
            break;
        }
        
        reject(new Error(message));
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 600000, // 10 minutes
      }
    );
  });
}

/**
 * Geocode a location name to coordinates using OpenStreetMap Nominatim API
 * @param location - Location name to geocode
 * @returns Promise resolving to location info
 */
export async function geocodeLocation(location: string): Promise<LocationInfo> {
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}&limit=1`
    );
    
    if (!response.ok) {
      throw new Error(`Geocoding request failed: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data || data.length === 0) {
      throw new Error(`Location "${location}" not found.`);
    }
    
    const result = data[0];
    const latitude = parseFloat(result.lat);
    const longitude = parseFloat(result.lon);
    
    if (isNaN(latitude) || isNaN(longitude)) {
      throw new Error('Invalid coordinates received from geocoding service.');
    }
    
    // Estimate timezone based on longitude (rough approximation)
    const timezone = Math.round(longitude / 15);
    
    return {
      name: result.display_name || location,
      coordinates: {
        latitude,
        longitude,
        timezone,
      },
    };
  } catch (error) {
    throw new Error(`Geocoding failed: ${error.message}`);
  }
}

/**
 * Reverse geocode coordinates to a location name
 * @param coordinates - Coordinates to reverse geocode
 * @returns Promise resolving to location name
 */
export async function reverseGeocodeLocation(coordinates: Coordinates): Promise<string> {
  try {
    const { latitude, longitude } = coordinates;
    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
    );
    
    if (!response.ok) {
      throw new Error(`Reverse geocoding request failed: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data || !data.display_name) {
      throw new Error('Unable to determine location name from coordinates.');
    }
    
    return data.display_name;
  } catch (error) {
    throw new Error(`Reverse geocoding failed: ${error.message}`);
  }
}

/**
 * Calculate timezone offset from coordinates (rough estimation)
 * This is a simple estimation and may not be accurate for all locations
 * For production use, consider using a proper timezone API
 * @param longitude - Longitude coordinate
 * @returns Estimated timezone offset in hours
 */
export function estimateTimezone(longitude: number): number {
  return Math.round(longitude / 15);
}

/**
 * Validate coordinates
 * @param coordinates - Coordinates to validate
 * @returns Boolean indicating if coordinates are valid
 */
export function validateCoordinates(coordinates: Coordinates): boolean {
  const { latitude, longitude } = coordinates;
  
  return (
    typeof latitude === 'number' &&
    typeof longitude === 'number' &&
    !isNaN(latitude) &&
    !isNaN(longitude) &&
    latitude >= -90 &&
    latitude <= 90 &&
    longitude >= -180 &&
    longitude <= 180
  );
}
