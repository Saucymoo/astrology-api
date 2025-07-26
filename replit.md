# Astrology Chart API

## Overview

This is a Python FastAPI backend service that generates personalized astrology charts based on user birth information. The API accepts birth details (name, date, time, location) and returns comprehensive astrological data including planetary positions, houses, and key placements like Sun, Moon, and Rising signs.

## User Preferences

Preferred communication style: Simple, everyday language.
Project Focus: Backend API for programmatic use, not web interface.

## System Architecture

### Backend Architecture (Python FastAPI)
- **FastAPI** framework with Python 3.11
- **Pydantic** models for type safety and validation
- **Uvicorn** ASGI server for high performance
- RESTful API design with comprehensive endpoints
- External API integration with Free Astrology API for chart calculations
- Geocoding service integration using OpenStreetMap Nominatim API
- Comprehensive error handling and logging

### Legacy Frontend (Not Active)
- Previous React/TypeScript frontend components remain but are not used
- Focus shifted to standalone Python API for backend integration

## Key Components

### Core API Endpoints
1. **POST /generate-chart** - Main endpoint for astrology chart generation
2. **POST /geocode** - Location name to coordinates conversion
3. **GET /health** - Health check and monitoring
4. **GET /planets** - List of supported celestial bodies
5. **GET /zodiac-signs** - List of zodiac signs

### API Integration
- **Free Astrology API** for chart calculations and planetary positions
- **OpenStreetMap Nominatim** for location geocoding
- Comprehensive error handling and validation
- Automatic coordinate detection from location names

### Data Models
- **BirthInfoRequest**: Validated birth information input
- **AstrologyResponse**: Complete chart with planets, houses, ascendant
- **Planet**: Individual planetary position and attributes
- **House**: Astrological house cusp information
- **Ascendant**: Rising sign details

## Data Flow

1. **API Request**: Birth information received via POST request
2. **Validation**: Pydantic models validate input data format
3. **Geocoding**: Location converted to coordinates if not provided
4. **API Call**: Birth data sent to Free Astrology API for calculations
5. **Processing**: Raw API response parsed into structured format
6. **Response**: Complete astrology chart returned as JSON

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