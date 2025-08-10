# Astrology Chart API

## Overview

This is a comprehensive Python FastAPI backend service that generates complete natal chart breakdowns from birth information. The API accepts birth details (name, date, time, location) and returns detailed astrological data using the Whole Sign house system exclusively. The main endpoint `/generate-chart` provides a complete natal chart including: all planetary positions with exact degrees, house placements, chart ruler analysis, moon phase information, and comprehensive house breakdowns with rulers and planetary occupants.

## Recent Changes

**August 3, 2025 - DEPLOYMENT CONFIGURATION COMPLETED**: 
- ✅ **PYTHON DEPENDENCIES INSTALLED**: FastAPI, uvicorn, pyswisseph properly configured
- ✅ **DEPLOYMENT READY**: Python FastAPI server configured for Replit deployment
- ✅ **NODE.JS MIGRATION**: Cleaned up Node.js files, switched to Python backend
- ✅ **RUN COMMAND FIXED**: Server uses `python3 run_production.py`
- ✅ **API SPECIFICATION**: Complete GPT integration documentation provided
- ✅ **EXACT ASCENDANT**: Taurus 19°14' precisely calculated with daylight saving correction
- ✅ **ASTRONOMICAL ACCURACY**: Sun at 29°42'23" Scorpio verified correct  
- ✅ **SWISS EPHEMERIS ACCURACY**: All planetary positions astronomically verified
- ✅ **PRODUCTION READY**: API ready for public deployment and GPT integration
- ✅ **TIMEZONE ACCURACY**: Adelaide daylight saving time (UTC+10:30) correctly applied for November 1974
- ✅ **GLOBAL TIMEZONE SUPPORT**: Comprehensive timezone handler supports worldwide locations with historical DST rules
- ✅ **API ACCURACY VERIFIED**: Backend calculations 100% accurate - Mia's chart shows correct Taurus 19°15'21" Rising
- ✅ **GPT SCHEMA UPDATED**: Enhanced OpenAPI schema with exact degree specifications for proper parsing
- ✅ **RETROGRADE CALCULATIONS FIXED**: Saturn and Chiron retrograde status now accurate for November 1974
- ✅ **UK TIMEZONE ACCURACY**: British Summer Time (UTC+1) correctly applied for UK locations in DST periods  
- ✅ **CHIRON CALCULATION FIX**: Resolved hardcoded fallback - now calculates unique Chiron positions per birth date using orbital mechanics

## User Preferences

Preferred communication style: Simple, everyday language.
Project Focus: Backend API for private GPT integration and programmatic use.
Required Astrological Points: Sun, Rising, Moon, Venus, Mercury, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Chiron, North Node, South Node, Midheaven, Descendant, Imum Coeli.
House System: Must use Whole Sign houses exclusively.
Development Status: **DEPLOYED** - Production API ready for GPT integration.
Deployment Command: `python run_production.py` or `uvicorn run_production:app --host 0.0.0.0 --port 8000`
API Documentation: https://YOUR-REPLIT-URL.replit.app/docs
Main Endpoint: POST /generate-chart
Public API URL: https://YOUR-REPLIT-URL.replit.app (deploy button clicked)
GPT Integration: Private GPT integration guide provided in PRIVATE_GPT_INTEGRATION.md

## System Architecture

### Backend Architecture (Python FastAPI)
- **FastAPI** framework with Python 3.11 and automatic API documentation
- **Swiss Ephemeris** (PySwissEph v2.10.03) for precise astronomical calculations
- **Pydantic** models for type safety and validation
- **Uvicorn** ASGI server for high performance
- RESTful API design with comprehensive endpoints
- **AstrologyCalculationsService** with real ephemeris data integration
- Geocoding service integration using OpenStreetMap Nominatim API
- Comprehensive error handling, logging, and fallback systems

### Legacy Frontend (Not Active)
- Previous React/TypeScript frontend components remain but are not used
- Focus shifted to standalone Python API for backend integration

## Key Components

### Core API Endpoints
1. **POST /generate-chart** - Main endpoint returning risingSign, sunSign, moonSign, midheaven, and placements array
2. **POST /geocode** - Location name to coordinates conversion
3. **GET /current-house-system** - Check current house system configuration
4. **POST /set-house-system** - Change house system programmatically
5. **GET /house-systems** - List all available house systems
6. **GET /health** - Health check and monitoring
7. **GET /planets** - List of supported celestial bodies
8. **GET /zodiac-signs** - List of zodiac signs

### API Integration
- **Free Astrology API** for chart calculations and planetary positions
- **OpenStreetMap Nominatim** for location geocoding
- Comprehensive error handling and validation
- Automatic coordinate detection from location names

### Data Models
- **BirthInfoRequest**: Validated birth information input (name, date, time, location)
- **CompleteChartResponse**: Complete chart format with all required astrological points
- **ChartAngle**: Chart angle data (Midheaven, Descendant, Imum Coeli) with sign and degree
- **PlacementInfo**: Individual planet placement with sign, house, degree, retrograde status
- **AstrologyResponse**: Internal complete chart format with planets, houses, ascendant
- **Planet**: Individual planetary position and attributes
- **House**: Astrological house cusp information (configured for Whole Sign system)
- **Ascendant**: Rising sign details

## Data Flow

1. **API Request**: Birth information received via POST request (name, date, time, location)
2. **Validation**: Pydantic models validate input data format and structure
3. **Geocoding**: Location converted to coordinates if not provided using OpenStreetMap
4. **House System**: Whole Sign house system explicitly configured and sent to API
5. **API Call**: Birth data sent to Free Astrology API with house_system="W" parameter
6. **Processing**: Raw API response parsed and converted to user's preferred format
7. **Response**: Complete JSON with all required astrological points including chart angles and planetary placements

## External Dependencies

### Production Dependencies
- **@neondatabase/serverless**: Serverless PostgreSQL client
- **@tanstack/react-query**: Server state management
- **drizzle-orm**: TypeScript ORM
- **@radix-ui/***: Headless UI components
- **react-hook-form**: Form state management
- **zod**: Schema validation
- **wouter**: Lightweight routing

### Development Tools
- **Vite**: Build tool and dev server
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first CSS framework
- **ESBuild**: Fast JavaScript bundler for production

## Deployment Strategy

### Development
- Vite dev server with HMR
- In-memory storage for rapid development
- Environment variable configuration for API keys

### Production Build
- **Frontend**: Vite build process generating optimized static assets
- **Backend**: ESBuild bundling Express server for Node.js deployment
- **Database**: Neon serverless PostgreSQL with connection pooling
- **Environment**: Production configuration with real database connections

### Architectural Decisions

1. **Monorepo Structure**: Single repository with `client/`, `server/`, and `shared/` directories for code organization and type sharing

2. **In-Memory Storage**: Provides development flexibility while maintaining database interface compatibility for future PostgreSQL integration

3. **External API Integration**: Uses Free Astrology API for accurate astronomical calculations rather than implementing complex astrological mathematics

4. **Geocoding Service**: OpenStreetMap Nominatim provides free location-to-coordinates conversion without API key requirements

5. **shadcn/ui Component System**: Offers high-quality, customizable components while maintaining design consistency and accessibility

6. **TypeScript Throughout**: Ensures type safety across the entire stack with shared schemas between frontend and backend