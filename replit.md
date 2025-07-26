# Astrology Chart Generator

## Overview

This is a full-stack web application that generates personalized astrology charts based on user birth information. The application uses modern web technologies including React, TypeScript, Express.js, and Drizzle ORM with PostgreSQL for data persistence.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **React 18** with TypeScript for the user interface
- **Vite** as the build tool and development server
- **TanStack Query (React Query)** for server state management and API calls
- **Wouter** for client-side routing (lightweight React Router alternative)
- **Tailwind CSS** with **shadcn/ui** components for styling
- **React Hook Form** with Zod validation for form handling

### Backend Architecture
- **Express.js** server with TypeScript
- RESTful API design with `/api/astrology/chart` endpoints
- In-memory storage implementation with interface for future database integration
- External API integration with Free Astrology API for chart calculations
- Geocoding service integration using OpenStreetMap Nominatim API

### Data Storage Solutions
- **Drizzle ORM** configured for PostgreSQL with schema definitions
- **Neon Database** serverless PostgreSQL for production
- In-memory storage fallback during development
- Database migrations managed through Drizzle Kit

## Key Components

### Core Features
1. **Birth Information Form** - Collects name, date, time, and location
2. **Chart Generation** - Processes birth data and calls astrology API
3. **Chart Display** - Renders planetary positions, houses, and astrological data
4. **Responsive Design** - Mobile-first approach with Tailwind CSS

### API Integration
- **Free Astrology API** for chart calculations
- **OpenStreetMap Nominatim** for location geocoding
- Error handling and validation for external service failures

### UI Components
- Comprehensive shadcn/ui component library
- Form components with validation feedback
- Loading states and error handling
- Toast notifications for user feedback

## Data Flow

1. **User Input**: Birth information entered through validated form
2. **Geocoding**: Location converted to coordinates if not provided
3. **API Call**: Birth data sent to astrology service for chart calculation
4. **Data Storage**: Chart results stored in database with user information
5. **Display**: Processed chart data rendered in organized, readable format

### Database Schema
- **Users Table**: Basic user information (id, username, password)
- **Birth Charts Table**: Chart data (id, name, birth details, coordinates, chart_data, timestamps)

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