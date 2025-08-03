# Astrology Chart API

A complete Python FastAPI backend service for generating personalized astrology charts.

## API Endpoint

**Live API**: `https://workspace.miamitchell1974.repl.co/generate-chart`

## Features

- **Complete Natal Chart Breakdown**: Comprehensive astrological analysis
  - 13 Planetary Bodies: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Chiron, North Node, South Node
  - Chart Angles: Rising (exact degree), Midheaven, Descendant, Imum Coeli
  - Each planet shows sign, house (1-12), and exact degree format
  
- **Advanced Analysis**:
  - Chart ruler identification based on Rising sign
  - Moon phase calculation with illumination percentage
  - Void-of-course Moon status
  - House rulers for each planetary placement
  - Complete house breakdown with occupying planets

- **Whole Sign House System**: Exclusively configured for traditional accuracy
- **No Authentication**: Public API ready for integration
- **Enhanced JSON Format**: Detailed, structured responses with exact degree formatting

## Usage

```bash
POST https://workspace.miamitchell1974.repl.co/generate-chart
Content-Type: application/json

{
  "name": "User Name",
  "date": "1990-06-15",
  "time": "14:30",
  "location": "New York, NY, USA"
}
```

## Response Format

```json
{
  "risingSign": "Sagittarius",
  "sunSign": "Libra",
  "moonSign": "Capricorn",
  "ascendant": {
    "sign": "Sagittarius",
    "degree": 19.16,
    "exactDegree": "19°09'36\""
  },
  "midheaven": {
    "sign": "Virgo", 
    "degree": 0.0,
    "exactDegree": "0°00'00\""
  },
  "chartRuler": {
    "planet": "Jupiter",
    "sign": "Capricorn",
    "house": 1,
    "degree": 15.25,
    "exactDegree": "15°15'00\"",
    "retrograde": false
  },
  "moonPhase": {
    "phaseName": "New Moon",
    "illumination": 0.0,
    "isVoidOfCourse": false,
    "nextAspect": null
  },
  "placements": [
    {
      "planet": "Sun",
      "sign": "Libra",
      "house": 3,
      "degree": 20.33,
      "exactDegree": "20°19'47\"",
      "retrograde": false,
      "houseRuler": "Saturn"
    }
    // ... continues with all 13 planetary bodies
  ],
  "houses": [
    {
      "house": 1,
      "sign": "Sagittarius",
      "ruler": "Jupiter",
      "planets": ["Jupiter", "North Node"]
    }
    // ... continues with all 12 houses
  ],
  "houseSystem": "W"
}
```

## Development

- **Framework**: FastAPI with Python 3.11
- **Testing**: Complete test suite in `test_*.py` files
- **Deployment**: Ready for Replit deployment
- **Documentation**: Available at `/docs` endpoint

## Status

✓ Fully functional and tested  
✓ Ready for production use  
✓ All requirements implemented  
✓ GPT integration ready