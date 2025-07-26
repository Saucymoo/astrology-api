# Astrology Chart API

A complete Python FastAPI backend service for generating personalized astrology charts.

## API Endpoint

**Live API**: `https://workspace.miamitchell1974.repl.co/generate-chart`

## Features

- **Complete Coverage**: All 17 required astrological points
  - 11 Planetary Bodies: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Chiron
  - 2 Lunar Nodes: North Node, South Node
  - 4 Chart Angles: Rising, Midheaven, Descendant, Imum Coeli

- **Whole Sign House System**: Exclusively configured
- **No Authentication**: Public API ready for integration
- **JSON Format**: Clean, structured responses

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
  "risingSign": "Taurus",
  "sunSign": "Sagittarius",
  "moonSign": "Pisces",
  "midheaven": {"sign": "Aquarius", "degree": 0.0},
  "descendant": {"sign": "Scorpio", "degree": 0.0},
  "imumCoeli": {"sign": "Leo", "degree": 0.0},
  "placements": [
    {
      "planet": "Sun",
      "sign": "Sagittarius",
      "house": 4,
      "degree": 10.03,
      "retrograde": false
    }
    // ... continues with all 13 planetary bodies
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