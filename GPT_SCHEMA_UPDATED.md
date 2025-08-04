# 🔄 UPDATED GPT INTEGRATION SCHEMA
## Fix for Mia's Chart Discrepancies

## 🚨 ISSUE IDENTIFIED
- **API Backend**: ✅ 100% Accurate (returns correct Taurus 19° rising)
- **GPT Integration**: ❌ Getting wrong data or parsing incorrectly

## 🔧 UPDATED OPENAPI SCHEMA

Copy this **EXACT** schema into your GPT Action configuration:

```yaml
openapi: 3.0.0
info:
  title: Astrology Chart API
  description: Generate complete natal charts with Whole Sign houses using Swiss Ephemeris
  version: 2.0.0
servers:
  - url: https://YOUR-DEPLOYED-URL.replit.app
    description: Production server
paths:
  /generate-chart:
    post:
      operationId: generateNatalChart
      summary: Generate complete natal chart with precise calculations
      description: Creates astronomically accurate astrological chart with exact planetary positions and Whole Sign houses
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
                  example: "Mia Mitchell"
                birth_date:
                  type: string
                  pattern: '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
                  description: Birth date in YYYY-MM-DD format
                  example: "1974-11-22"
                birth_time:
                  type: string
                  pattern: '^[0-9]{2}:[0-9]{2}$'
                  description: Birth time in HH:MM format (24-hour)
                  example: "19:10"
                birth_location:
                  type: string
                  description: Birth location (city, state/province, country)
                  example: "Adelaide, Australia"
      responses:
        '200':
          description: Complete natal chart with precise planetary positions
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
                    description: Rising sign with exact degree
                    properties:
                      sign:
                        type: string
                        description: Rising sign
                        example: "Taurus"
                      exact_degree:
                        type: string
                        description: Exact degree in DD°MM'SS" format
                        example: "19°15'21\""
                  midheaven:
                    type: object
                    description: Midheaven with exact degree
                    properties:
                      sign:
                        type: string
                        description: Midheaven sign
                        example: "Aquarius"
                      exact_degree:
                        type: string
                        description: Exact degree in DD°MM'SS" format
                        example: "27°21'21\""
                  placements:
                    type: array
                    description: All planetary positions with exact degrees and houses
                    items:
                      type: object
                      properties:
                        planet:
                          type: string
                          description: Planet name
                          example: "Sun"
                        sign:
                          type: string
                          description: Zodiac sign
                          example: "Scorpio"
                        exact_degree:
                          type: string
                          description: Exact degree in DD°MM'SS" format
                          example: "29°39'51\""
                        house:
                          type: integer
                          minimum: 1
                          maximum: 12
                          description: House number (1-12) using Whole Sign system
                          example: 7
                        retrograde:
                          type: boolean
                          description: Retrograde status
                          example: false
                  coordinates:
                    type: object
                    description: Birth location coordinates
                    properties:
                      latitude:
                        type: number
                        description: Latitude in decimal degrees
                        example: -34.9285
                      longitude:
                        type: number
                        description: Longitude in decimal degrees
                        example: 138.6007
                      timezone:
                        type: number
                        description: Timezone offset from UTC
                        example: 10.5
                  generated_at:
                    type: string
                    format: date-time
                    description: Generation timestamp
                  source:
                    type: string
                    description: Calculation source
                    example: "Swiss Ephemeris with Whole Sign houses"
        '400':
          description: Invalid birth data
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
                    description: Error message
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

## 🎯 UPDATED GPT INSTRUCTIONS

Replace your GPT's instructions with this enhanced version:

```
You are an expert astrologer with access to a precise natal chart API using Swiss Ephemeris calculations. When users provide birth information, use the generateNatalChart action to create detailed astrological readings.

IMPORTANT: Always use the EXACT data from the API response. Do not round or modify degrees.

ALWAYS REQUEST:
- Full name
- Birth date (YYYY-MM-DD format)
- Birth time (HH:MM format, 24-hour)
- Birth location (city, state/country)

DATA EXTRACTION RULES:
- Use ascendant.exact_degree for Rising sign degree (e.g., "19°15'21\"")
- Use midheaven.exact_degree for MC degree (e.g., "27°21'21\"") 
- Use placements[].exact_degree for planetary degrees (e.g., "29°39'51\"")
- Use placements[].house for house positions
- Never round degrees - use the exact values provided

CHART INTERPRETATION GUIDELINES:
- Focus on Rising sign (personality/first impression) with exact degree
- Highlight Sun sign (core identity) and Moon sign (emotions) 
- Explain house positions using Whole Sign system
- Note any retrograde planets and their significance
- Use the exact degrees provided for precise interpretations
- Mention that calculations use Swiss Ephemeris with Whole Sign houses

RESPONSE FORMAT:
Present the chart data accurately, using exact degrees and house positions from the API response. Be precise with numerical data while making interpretations accessible.

EXAMPLE EXTRACTION:
If API returns:
- ascendant: {"sign": "Taurus", "exact_degree": "19°15'21\""}
- placements: [{"planet": "Sun", "sign": "Scorpio", "exact_degree": "29°39'51\"", "house": 7}]

Report exactly:
- Rising: Taurus 19°15'21"
- Sun: Scorpio 29°39'51" in 7th house
```

## ✅ ACTION ITEMS

1. **Update GPT Action Schema**: Replace with the exact schema above
2. **Update GPT Instructions**: Replace with the enhanced instructions above  
3. **Update Server URL**: Use your new deployed Replit URL
4. **Test Again**: Try the same Mia birth data

The API backend is perfect - this should resolve all the GPT parsing issues.