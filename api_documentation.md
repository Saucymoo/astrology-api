# Astrology Chart API Documentation

## Public API Endpoint

**Base URL:** `http://localhost:8000` (when running locally)
**Production URL:** Will be available on Replit deployment

## Main Endpoint: Generate Chart

### POST /generate-chart

Generate a complete natal chart with all planetary positions and house placements using the Whole Sign house system.

#### Request Format

```json
{
  "name": "Full Name",
  "birth_date": "YYYY-MM-DD",
  "birth_time": "HH:MM",
  "birth_location": "City, State/Province, Country"
}
```

#### Request Fields

- **name** (string, required): Full name of the person
- **birth_date** (string, required): Birth date in YYYY-MM-DD format
- **birth_time** (string, required): Birth time in HH:MM (24-hour format)
- **birth_location** (string, required): Birth location (city, state/province, country)

#### Response Format

```json
{
  "name": "Full Name",
  "birth_date": "YYYY-MM-DD",
  "birth_time": "HH:MM",
  "birth_location": "City, State/Province, Country",
  "coordinates": {
    "latitude": -34.9285,
    "longitude": 138.6007,
    "timezone": 9.5
  },
  "house_system": "Whole Sign",
  "ascendant": {
    "sign": "Taurus",
    "degree": 19.233333,
    "exact_degree": "19°14'00\""
  },
  "midheaven": {
    "sign": "Aquarius", 
    "degree": 15.0,
    "exact_degree": "15°00'00\""
  },
  "rising_sign": "Taurus",
  "sun_sign": "Scorpio",
  "moon_sign": "Pisces",
  "placements": [
    {
      "planet": "Sun",
      "sign": "Scorpio",
      "degree": 29.706452,
      "exact_degree": "29°42'23\"",
      "house": 7,
      "retrograde": false
    },
    {
      "planet": "Moon",
      "sign": "Pisces", 
      "degree": 4.700195,
      "exact_degree": "4°42'00\"",
      "house": 11,
      "retrograde": false
    }
    // ... continues for all 13 planets
  ],
  "generated_at": "2025-08-03T11:22:33.123456",
  "source": "Swiss Ephemeris with Whole Sign Houses"
}
```

#### Response Fields

- **name**: Person's name
- **birth_date**: Birth date in YYYY-MM-DD format
- **birth_time**: Birth time in HH:MM format  
- **birth_location**: Full birth location
- **coordinates**: Latitude, longitude, and timezone
- **house_system**: Always "Whole Sign"
- **ascendant**: Rising sign with exact degree
- **midheaven**: Midheaven (MC) sign with exact degree
- **rising_sign**: Rising sign name
- **sun_sign**: Sun sign name
- **moon_sign**: Moon sign name
- **placements**: Array of all planetary positions
  - **planet**: Planet name (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, North Node, South Node, Chiron)
  - **sign**: Zodiac sign
  - **degree**: Exact decimal degree
  - **exact_degree**: Formatted degree (DD°MM'SS")
  - **house**: House number (1-12) 
  - **retrograde**: Boolean indicating retrograde motion
- **generated_at**: ISO timestamp of generation
- **source**: Calculation source (Swiss Ephemeris)

## Sample Requests

### cURL Example

```bash
curl -X POST "http://localhost:8000/generate-chart" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "birth_date": "1990-06-15", 
    "birth_time": "14:30",
    "birth_location": "New York, NY, USA"
  }'
```

### JavaScript fetch() Example

```javascript
const response = await fetch('http://localhost:8000/generate-chart', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'John Doe',
    birth_date: '1990-06-15',
    birth_time: '14:30', 
    birth_location: 'New York, NY, USA'
  })
});

const chart = await response.json();
console.log(chart);
```

### Python requests Example

```python
import requests

response = requests.post('http://localhost:8000/generate-chart', json={
    'name': 'John Doe',
    'birth_date': '1990-06-15',
    'birth_time': '14:30',
    'birth_location': 'New York, NY, USA'
})

chart = response.json()
print(chart)
```

## Additional Endpoints

### GET /
API information and available endpoints

### GET /health
Health check and system status

### GET /planets  
List of supported planets and celestial bodies

### GET /zodiac-signs
List of zodiac signs

### GET /house-system
Information about the house system used

### GET /docs
Interactive API documentation (Swagger UI)

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Could not find coordinates for location: InvalidCity"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["birth_date"],
      "msg": "string does not match regex \"^\\d{4}-\\d{2}-\\d{2}$\"",
      "type": "value_error.regex"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to generate chart: calculation error"
}
```

## Features

✅ **Astronomical Accuracy**: Uses Swiss Ephemeris for precise planetary calculations
✅ **Whole Sign Houses**: Exclusively uses traditional Whole Sign house system
✅ **International Support**: Handles worldwide locations with automatic geocoding
✅ **Complete Data**: Returns all major planets, nodes, and chart angles
✅ **Exact Degrees**: Provides both decimal and formatted degree notations
✅ **Retrograde Status**: Accurate retrograde calculations for all planets
✅ **CORS Enabled**: Ready for frontend integration
✅ **Auto Documentation**: Interactive API docs at /docs endpoint