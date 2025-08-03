# 🔗 GPT INTEGRATION SPECIFICATION
## Astrology Chart API for Custom Actions & Plugins

## 🌐 PUBLIC API URL
**Production URL:** `https://YOUR-REPLIT-URL.replit.app` (available after deployment)
**Endpoint:** `POST /generate-chart`
**Method:** POST
**Content-Type:** application/json

## 📝 REQUEST FORMAT

### JSON Body Example:
```json
{
  "name": "John Doe",
  "birth_date": "1990-06-15",
  "birth_time": "14:30",
  "birth_location": "New York, NY, USA"
}
```

### Required Fields:
- **name** (string): Full name of the person
- **birth_date** (string): Birth date in YYYY-MM-DD format
- **birth_time** (string): Birth time in HH:MM format (24-hour)
- **birth_location** (string): Birth location (city, state/province, country)

## 📊 RESPONSE STRUCTURE

### Complete JSON Response Keys:
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
    }
    // ... continues for all 13 planets
  ],
  "generated_at": "2025-08-03T15:30:45.123456",
  "source": "Swiss Ephemeris with Whole Sign Houses"
}
```

### Key Response Fields:

#### Chart Angles:
- **ascendant**: Rising sign with exact degree
- **midheaven**: Midheaven (MC) with exact degree  
- **rising_sign**: Rising sign name (string)

#### Primary Signs:
- **sun_sign**: Sun sign name (string)
- **moon_sign**: Moon sign name (string)

#### Planetary Data:
- **placements**: Array of all 13 celestial bodies
  - **planet**: Name (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, North Node, South Node, Chiron)
  - **sign**: Zodiac sign name
  - **degree**: Exact decimal degree
  - **exact_degree**: Formatted degree string (DD°MM'SS")
  - **house**: House number (1-12)
  - **retrograde**: Boolean for retrograde motion

#### System Info:
- **house_system**: Always "Whole Sign"
- **coordinates**: Location data with timezone
- **generated_at**: ISO timestamp
- **source**: Calculation method

## 🔧 GPT CUSTOM ACTION CONFIGURATION

### OpenAPI Schema for GPT:
```yaml
openapi: 3.0.0
info:
  title: Astrology Chart API
  version: 1.0.0
servers:
  - url: https://YOUR-REPLIT-URL.replit.app
paths:
  /generate-chart:
    post:
      summary: Generate complete natal chart
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [name, birth_date, birth_time, birth_location]
              properties:
                name:
                  type: string
                  description: Full name
                birth_date:
                  type: string
                  pattern: '^\\d{4}-\\d{2}-\\d{2}$'
                  description: Birth date (YYYY-MM-DD)
                birth_time:
                  type: string
                  pattern: '^\\d{2}:\\d{2}$'
                  description: Birth time (HH:MM)
                birth_location:
                  type: string
                  description: Birth location
      responses:
        '200':
          description: Complete natal chart
          content:
            application/json:
              schema:
                type: object
                properties:
                  name: {type: string}
                  rising_sign: {type: string}
                  sun_sign: {type: string}
                  moon_sign: {type: string}
                  house_system: {type: string}
                  ascendant: 
                    type: object
                    properties:
                      sign: {type: string}
                      exact_degree: {type: string}
                  placements:
                    type: array
                    items:
                      type: object
                      properties:
                        planet: {type: string}
                        sign: {type: string}
                        exact_degree: {type: string}
                        house: {type: integer}
                        retrograde: {type: boolean}
```

## 🎯 INTEGRATION EXAMPLES

### GPT Prompt Integration:
"When a user asks for their natal chart, use the astrology API with their birth information. Always request: name, birth date (YYYY-MM-DD), birth time (HH:MM), and birth location. Present the results in an engaging, interpretive format highlighting their rising sign, sun sign, moon sign, and key planetary placements with house positions."

### Sample GPT Response:
"Based on your birth information, here's your complete natal chart:

**Rising Sign:** Virgo 23°27' - Your outer personality and first impression
**Sun Sign:** Gemini 24°07' in 10th House - Your core identity and career focus  
**Moon Sign:** Pisces 8°39' in 7th House - Your emotional nature and relationships

**Key Planetary Positions:**
- Mercury in Cancer 12°34' (11th House) - Communication style
- Venus in Leo 6°45' (12th House) - Love and values
- Mars in Aries 18°22' (8th House) - Energy and drive

Your chart uses the traditional Whole Sign house system with astronomically precise calculations."

## 🚀 DEPLOYMENT STATUS

The API is ready for deployment on Replit. Once deployed:
1. You'll receive a public URL ending in `.replit.app`
2. The API will be accessible worldwide
3. No authentication required
4. CORS enabled for web integration
5. Automatic scaling and uptime management

Perfect for GPT Custom Actions, ChatGPT plugins, or any AI integration requiring accurate astrological data.