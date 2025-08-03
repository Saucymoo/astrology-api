# 🚀 ASTROLOGY API DEPLOYMENT INSTRUCTIONS

## DEPLOYMENT CONFIGURATION FIXED

Your astrology chart API is ready for deployment with the following configuration:

### ✅ PYTHON DEPENDENCIES INSTALLED
- fastapi==0.104.1
- uvicorn[standard]==0.24.0  
- python-multipart==0.0.6
- pydantic==2.5.0
- requests==2.31.0
- pyswisseph==2.10.03.2
- httpx==0.25.2

### ✅ SERVER CONFIGURATION
**Run Command:** `python3 run_production.py`
**Alternative:** `uvicorn run_production:app --host 0.0.0.0 --port 8000`
**Language:** Python 3.11
**Framework:** FastAPI

## 🌐 LIVE API SPECIFICATION

Once deployed, your API will be available at:
**URL:** `https://YOUR-REPLIT-URL.replit.app`

### MAIN ENDPOINT: POST /generate-chart

**Request Format:**
```json
{
  "name": "John Doe",
  "birth_date": "1990-06-15",
  "birth_time": "14:30",
  "birth_location": "New York, NY, USA"
}
```

**Response Format:**
```json
{
  "name": "John Doe",
  "birth_date": "1990-06-15",
  "birth_time": "14:30",
  "birth_location": "New York, NY, USA",
  "coordinates": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": -5
  },
  "house_system": "Whole Sign",
  "ascendant": {
    "sign": "Virgo",
    "degree": 23.456789,
    "exact_degree": "23°27'24\""
  },
  "midheaven": {
    "sign": "Gemini",
    "degree": 15.0,
    "exact_degree": "15°00'00\""
  },
  "rising_sign": "Virgo",
  "sun_sign": "Gemini",
  "moon_sign": "Pisces",
  "placements": [
    {
      "planet": "Sun",
      "sign": "Gemini",
      "degree": 24.123456,
      "exact_degree": "24°07'24\"",
      "house": 10,
      "retrograde": false
    },
    {
      "planet": "Moon",
      "sign": "Pisces", 
      "degree": 8.654321,
      "exact_degree": "8°39'15\"",
      "house": 7,
      "retrograde": false
    },
    {
      "planet": "Mercury",
      "sign": "Cancer",
      "degree": 12.345678,
      "exact_degree": "12°20'44\"", 
      "house": 11,
      "retrograde": false
    },
    {
      "planet": "Venus",
      "sign": "Leo",
      "degree": 6.789012,
      "exact_degree": "6°47'20\"",
      "house": 12,
      "retrograde": false
    },
    {
      "planet": "Mars",
      "sign": "Aries",
      "degree": 18.234567,
      "exact_degree": "18°14'04\"",
      "house": 8,
      "retrograde": false
    },
    {
      "planet": "Jupiter",
      "sign": "Cancer",
      "degree": 25.678901,
      "exact_degree": "25°40'44\"",
      "house": 11,
      "retrograde": false
    },
    {
      "planet": "Saturn",
      "sign": "Capricorn",
      "degree": 14.567890,
      "exact_degree": "14°34'04\"",
      "house": 5,
      "retrograde": false
    },
    {
      "planet": "Uranus",
      "sign": "Capricorn",
      "degree": 8.901234,
      "exact_degree": "8°54'04\"",
      "house": 5,
      "retrograde": false
    },
    {
      "planet": "Neptune",
      "sign": "Capricorn",
      "degree": 13.456789,
      "exact_degree": "13°27'24\"",
      "house": 5,
      "retrograde": false
    },
    {
      "planet": "Pluto",
      "sign": "Scorpio",
      "degree": 16.789012,
      "exact_degree": "16°47'20\"",
      "house": 3,
      "retrograde": false
    },
    {
      "planet": "North Node",
      "sign": "Aquarius",
      "degree": 27.123456,
      "exact_degree": "27°07'24\"",
      "house": 6,
      "retrograde": false
    },
    {
      "planet": "South Node",
      "sign": "Leo",
      "degree": 27.123456,
      "exact_degree": "27°07'24\"",
      "house": 12,
      "retrograde": false
    },
    {
      "planet": "Chiron",
      "sign": "Cancer",
      "degree": 3.567890,
      "exact_degree": "3°34'04\"",
      "house": 11,
      "retrograde": false
    }
  ],
  "generated_at": "2025-08-03T15:45:00.123456",
  "source": "Swiss Ephemeris with Whole Sign Houses"
}
```

## 🔧 DEPLOYMENT STEPS

1. **Click Deploy Button** in Replit interface
2. **Choose Autoscale Deployment**
3. **Verify Run Command:** Should use `python3 run_production.py`
4. **Get Public URL:** Will be `https://YOUR-REPLIT-URL.replit.app`
5. **Test Endpoint:** POST to `/generate-chart`

## 📝 SAMPLE REQUESTS FOR GPT INTEGRATION

### cURL:
```bash
curl -X POST "https://YOUR-REPLIT-URL.replit.app/generate-chart" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "birth_date": "1990-06-15", 
    "birth_time": "14:30",
    "birth_location": "New York, NY, USA"
  }'
```

### JavaScript fetch():
```javascript
const response = await fetch('https://YOUR-REPLIT-URL.replit.app/generate-chart', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    birth_date: '1990-06-15',
    birth_time: '14:30', 
    birth_location: 'New York, NY, USA'
  })
});
const chart = await response.json();
```

### Python requests:
```python
import requests

chart = requests.post('https://YOUR-REPLIT-URL.replit.app/generate-chart', json={
    'name': 'John Doe',
    'birth_date': '1990-06-15',
    'birth_time': '14:30',
    'birth_location': 'New York, NY, USA'
}).json()

print(f"Rising: {chart['ascendant']['sign']} {chart['ascendant']['exact_degree']}")
```

## ✅ VERIFIED FEATURES

- **Swiss Ephemeris Accuracy:** All calculations use real astronomical data
- **Whole Sign Houses:** Traditional house system properly implemented
- **Complete Planet Set:** All 13 required celestial bodies included
- **Exact Degrees:** Precise positions formatted as DD°MM'SS"
- **House Assignments:** Correct house numbers (1-12) for each planet
- **Retrograde Status:** Accurate retrograde detection
- **International Locations:** Worldwide geocoding support
- **CORS Enabled:** Ready for frontend integration

## 🎯 GPT INTEGRATION READY

Your API provides everything needed for GPT Custom Actions:
- Clean JSON response structure
- All major astrological points
- Exact degree formatting
- House system specification
- Astronomically accurate calculations

The system has been tested and verified with your exact specifications (Taurus 19°14' Ascendant, Scorpio 29°42'23" Sun) and is ready for production deployment.