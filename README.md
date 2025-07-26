# Astrology Chart API

A FastAPI backend service that generates personalized astrology charts from birth information using external astrology APIs.

## Features

- **Birth Chart Generation**: Generate complete astrology charts with planetary positions, houses, and key placements
- **Geocoding Support**: Automatic conversion of location names to coordinates
- **Comprehensive Data**: Sun, Moon, Rising signs plus all planetary positions
- **RESTful API**: Clean, well-documented endpoints
- **Type Safety**: Full Pydantic model validation
- **Error Handling**: Robust error handling with detailed messages

## API Endpoints

### Core Endpoints

- `POST /generate-chart` - Generate astrology chart from birth information
- `POST /geocode` - Convert location name to coordinates
- `GET /health` - Health check endpoint
- `GET /` - API information

### Metadata Endpoints

- `GET /planets` - List supported planets and celestial bodies
- `GET /zodiac-signs` - List all zodiac signs

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn pydantic requests python-multipart
   ```

2. **Run the API**:
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

3. **View Documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Usage Examples

### Generate Astrology Chart

```python
import requests

# Birth information
birth_data = {
    "name": "John Doe",
    "date": "1990-06-15",        # YYYY-MM-DD format
    "time": "14:30",             # HH:MM format (24-hour)
    "location": "New York, NY, USA"
}

# Generate chart
response = requests.post(
    "http://localhost:8000/generate-chart",
    json=birth_data
)

chart = response.json()
print(f"Sun Sign: {chart['planets'][0]['sign']}")
print(f"Rising Sign: {chart['ascendant']['sign']}")
```

### Using cURL

```bash
curl -X POST "http://localhost:8000/generate-chart" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "date": "1990-06-15",
       "time": "14:30",
       "location": "New York, NY, USA"
     }'
```

## Request Format

### Birth Information Request

```json
{
  "name": "John Doe",
  "date": "1990-06-15",
  "time": "14:30",
  "location": "New York, NY, USA",
  "latitude": 40.7128,     // Optional
  "longitude": -74.0060,   // Optional
  "timezone": -5           // Optional
}
```

## Response Format

### Astrology Chart Response

```json
{
  "success": true,
  "name": "John Doe",
  "birth_info": {
    "name": "John Doe",
    "date": "1990-06-15",
    "time": "14:30",
    "location": "New York, NY, USA",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": -5
  },
  "planets": [
    {
      "name": "Sun",
      "sign": "Gemini",
      "sign_num": 3,
      "degree": 24.5,
      "house": 10,
      "retro": false
    }
  ],
  "houses": [
    {
      "house": 1,
      "sign": "Leo",
      "sign_num": 5,
      "degree": 15.3
    }
  ],
  "ascendant": {
    "sign": "Leo",
    "degree": 15.3
  },
  "generated_at": "2025-01-26T12:00:00"
}
```

## Testing

Run the test script to verify functionality:

```bash
python test_api.py
```

The test script will validate:
- Health check endpoint
- Chart generation with sample data
- Geocoding functionality
- Metadata endpoints

## Architecture

### Project Structure

```
├── main.py                     # FastAPI application
├── models.py                   # Pydantic models
├── services/
│   ├── __init__.py
│   ├── astrology_service.py    # Chart generation logic
│   └── geocoding_service.py    # Location services
├── test_api.py                 # Test script
└── README.md                   # This file
```

### Key Components

- **FastAPI Application**: Main API server with CORS support
- **Pydantic Models**: Type-safe request/response models
- **Astrology Service**: Handles Free Astrology API integration
- **Geocoding Service**: Converts locations to coordinates
- **Comprehensive Testing**: Full test suite for validation

## External APIs Used

- **Free Astrology API**: Chart calculations and planetary positions
- **OpenStreetMap Nominatim**: Geocoding and location services

## Error Handling

The API provides detailed error messages for:
- Invalid date/time formats
- Location not found
- API service failures
- Network connectivity issues

## Customization

### Adding New Planets

Edit `astrology_service.py` to include additional celestial bodies:

```python
def get_supported_planets(self) -> List[str]:
    return [
        "Sun", "Moon", "Mercury", "Venus", "Mars",
        "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto",
        "North Node", "South Node", "Chiron",
        "Ceres", "Pallas", "Juno", "Vesta"  # Add asteroids
    ]
```

### Different Astrology APIs

Replace the API endpoint in `astrology_service.py`:

```python
def __init__(self):
    self.base_url = "https://your-preferred-api.com/api/v1"
```

## Production Considerations

- Add API rate limiting
- Implement caching for geocoding results
- Use proper timezone APIs instead of longitude estimation
- Add authentication if needed
- Set up monitoring and logging
- Configure CORS origins for security

## License

MIT License - Feel free to use and modify for your projects.