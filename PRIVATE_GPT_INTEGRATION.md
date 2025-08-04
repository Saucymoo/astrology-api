# 🔒 PRIVATE GPT INTEGRATION GUIDE
## Astrology Chart API for Custom GPT Actions

## 🌐 API ENDPOINT CONFIGURATION

**Production URL:** `https://mias-astrology-api-miamitchell1974.replit.app`
**Main Endpoint:** `POST /generate-chart`
**Authentication:** None required (public API)
**Content-Type:** `application/json`

## 📝 GPT CUSTOM ACTION SCHEMA

### OpenAPI Schema for GPT Actions:
```yaml
openapi: 3.0.0
info:
  title: Astrology Chart API
  description: Generate complete natal charts with Whole Sign houses using Swiss Ephemeris
  version: 1.0.0
servers:
  - url: https://mias-astrology-api-miamitchell1974.replit.app
paths:
  /generate-chart:
    post:
      operationId: generateNatalChart
      summary: Generate complete natal chart
      description: Creates a comprehensive astrological chart with planetary positions, houses, and degrees
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
                  description: Full name of the person
                  example: "John Doe"
                birth_date:
                  type: string
                  pattern: '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
                  description: Birth date in YYYY-MM-DD format
                  example: "1990-06-15"
                birth_time:
                  type: string
                  pattern: '^[0-9]{2}:[0-9]{2}$'
                  description: Birth time in HH:MM format (24-hour)
                  example: "14:30"
                birth_location:
                  type: string
                  description: Birth location (city, state/province, country)
                  example: "New York, NY, USA"
      responses:
        '200':
          description: Complete natal chart with planetary positions
          content:
            application/json:
              schema:
                type: object
                properties:
                  name: 
                    type: string
                    description: Person's name
                  birth_date:
                    type: string
                    description: Birth date
                  birth_time:
                    type: string
                    description: Birth time
                  birth_location:
                    type: string
                    description: Birth location
                  house_system:
                    type: string
                    description: House system used (always "Whole Sign")
                  rising_sign:
                    type: string
                    description: Ascendant/Rising sign
                  sun_sign:
                    type: string
                    description: Sun sign
                  moon_sign:
                    type: string
                    description: Moon sign
                  ascendant:
                    type: object
                    properties:
                      sign:
                        type: string
                        description: Rising sign
                      exact_degree:
                        type: string
                        description: Exact degree (DD°MM'SS")
                  midheaven:
                    type: object
                    properties:
                      sign:
                        type: string
                        description: Midheaven sign
                      exact_degree:
                        type: string
                        description: Exact degree (DD°MM'SS")
                  placements:
                    type: array
                    description: All planetary positions
                    items:
                      type: object
                      properties:
                        planet:
                          type: string
                          description: Planet name
                        sign:
                          type: string
                          description: Zodiac sign
                        exact_degree:
                          type: string
                          description: Exact degree (DD°MM'SS")
                        house:
                          type: integer
                          description: House number (1-12)
                        retrograde:
                          type: boolean
                          description: Retrograde status
                  coordinates:
                    type: object
                    properties:
                      latitude:
                        type: number
                      longitude:
                        type: number
                      timezone:
                        type: number
                  generated_at:
                    type: string
                    description: Generation timestamp
                  source:
                    type: string
                    description: Calculation source
        '500':
          description: Chart generation error
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
                    description: Error message
```

## 🎯 GPT INSTRUCTIONS

### System Prompt for Your Private GPT:
```
You are an expert astrologer with access to a comprehensive natal chart API. When users provide birth information, use the generateNatalChart action to create detailed astrological readings.

ALWAYS REQUEST:
- Full name
- Birth date (YYYY-MM-DD format)
- Birth time (HH:MM format, 24-hour)
- Birth location (city, state/country)

CHART INTERPRETATION GUIDELINES:
- Focus on Rising sign (personality/first impression)
- Highlight Sun sign (core identity) and Moon sign (emotions)
- Explain house positions and their meanings
- Note any retrograde planets and their significance
- Use the exact degrees provided for precise interpretations
- Mention the Whole Sign house system being used

RESPONSE FORMAT:
Present the chart data in an engaging, interpretive format that's accessible to non-astrologers while maintaining accuracy.
```

## 📊 SAMPLE REQUEST/RESPONSE

### Sample Request:
```json
{
  "name": "Sarah Johnson",
  "birth_date": "1985-03-20",
  "birth_time": "10:15",
  "birth_location": "London, UK"
}
```

### Sample GPT Integration:
**User:** "Can you generate my natal chart? I'm Sarah Johnson, born March 20, 1985 at 10:15 AM in London, UK."

**GPT Response:** "I'll generate your complete natal chart using Swiss Ephemeris calculations with the traditional Whole Sign house system.

*[Calls generateNatalChart action]*

**Your Natal Chart - Sarah Johnson**

**Rising Sign:** Gemini 15°23' - You present as curious, communicative, and adaptable. People see you as quick-witted and versatile.

**Sun in Pisces** (29°42') in the 10th House - Your core identity is intuitive and compassionate, with a strong focus on career and public image.

**Moon in Leo** (12°18') in the 3rd House - Emotionally, you need recognition and creative expression, particularly through communication.

**Key Planetary Positions:**
- Mercury in Aries 8°45' (11th House) - Direct, assertive communication style
- Venus in Taurus 22°31' (12th House) - Deep, sensual approach to love and values
- Mars in Gemini 5°12' (1st House) - Mental energy and versatile action

Your chart shows a blend of mutable signs emphasizing adaptability, with strong emphasis on communication (Gemini rising, Mars in 1st) balanced by deep intuition (Pisces Sun)."

## 🔧 INTEGRATION STEPS

1. **Create Custom GPT**
   - Go to GPT Builder in ChatGPT
   - Set up your astrology GPT with the system prompt above

2. **Add Custom Action**
   - In GPT configuration, go to "Actions"
   - Import the OpenAPI schema provided above
   - Set the server URL to your Replit deployment

3. **Test Integration**
   - Provide test birth data
   - Verify the API returns complete chart data
   - Ensure GPT interprets the results correctly

4. **Privacy Settings**
   - Set GPT to "Only me" for private use
   - Configure sharing settings as needed

## ✅ FEATURES CONFIRMED

- **Real Swiss Ephemeris data** - Astronomically accurate planetary positions
- **Whole Sign houses** - Traditional house system properly implemented
- **Complete planetary set** - All 13 major celestial bodies
- **Exact degrees** - Precise positions formatted as DD°MM'SS"
- **International locations** - Worldwide geocoding support
- **No authentication** - Public API ready for integration
- **JSON response** - Clean, structured data for GPT processing

Your private astrology GPT will provide accurate, personalized chart readings using real astronomical data calculated specifically for each user's birth information.