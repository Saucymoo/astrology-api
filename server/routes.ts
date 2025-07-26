import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { birthInfoSchema, chartResponseSchema } from "@shared/schema";
import { z } from "zod";

// Geocoding function to get coordinates from location name
async function getCoordinates(location: string): Promise<{ lat: number; lng: number; timezone: number }> {
  try {
    // Using a simple geocoding approach - in production, you might want to use a proper geocoding service
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}&limit=1`);
    const data = await response.json();
    
    if (data && data.length > 0) {
      const lat = parseFloat(data[0].lat);
      const lng = parseFloat(data[0].lon);
      
      // Simple timezone estimation based on longitude (rough approximation)
      const timezone = Math.round(lng / 15);
      
      return { lat, lng, timezone };
    }
    
    throw new Error("Location not found");
  } catch (error) {
    throw new Error(`Geocoding failed: ${error.message}`);
  }
}

// Function to call the Free Astrology API
async function getAstrologyChart(
  date: string, 
  time: string, 
  lat: number, 
  lng: number, 
  timezone: number
): Promise<any> {
  try {
    const [year, month, day] = date.split('-').map(Number);
    const [hour, minute] = time.split(':').map(Number);

    // API endpoint for birth chart
    const apiUrl = 'https://api.freeastrologyapi.com/api/v1/birth-chart';
    
    const requestBody = {
      day,
      month,
      year,
      hour,
      min: minute,
      lat,
      lon: lng,
      tzone: timezone
    };

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error(`Astrology API call failed: ${error.message}`);
  }
}

export async function registerRoutes(app: Express): Promise<Server> {
  // Get astrology chart endpoint
  app.post("/api/astrology/chart", async (req, res) => {
    try {
      // Validate request body
      const validatedData = birthInfoSchema.parse(req.body);
      
      let lat = validatedData.latitude;
      let lng = validatedData.longitude;
      let timezone = validatedData.timezone;

      // If coordinates not provided, geocode the location
      if (!lat || !lng || timezone === undefined) {
        const coords = await getCoordinates(validatedData.location);
        lat = coords.lat;
        lng = coords.lng;
        timezone = coords.timezone;
      }

      // Get astrology chart data
      const chartData = await getAstrologyChart(
        validatedData.date,
        validatedData.time,
        lat,
        lng,
        timezone
      );

      // Save to storage
      const savedChart = await storage.createBirthChart({
        name: validatedData.name,
        date: validatedData.date,
        time: validatedData.time,
        location: validatedData.location,
        latitude: lat,
        longitude: lng,
        timezone,
        chartData,
      });

      res.json({
        success: true,
        chart: savedChart,
        data: chartData,
      });
    } catch (error) {
      console.error('Chart generation error:', error);
      res.status(400).json({
        success: false,
        error: error.message || 'Failed to generate astrology chart',
      });
    }
  });

  // Get saved charts by name
  app.get("/api/astrology/charts/:name", async (req, res) => {
    try {
      const { name } = req.params;
      const charts = await storage.getBirthChartsByName(name);
      
      res.json({
        success: true,
        charts,
      });
    } catch (error) {
      console.error('Get charts error:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to retrieve charts',
      });
    }
  });

  // Get specific chart by ID
  app.get("/api/astrology/chart/:id", async (req, res) => {
    try {
      const { id } = req.params;
      const chart = await storage.getBirthChart(id);
      
      if (!chart) {
        return res.status(404).json({
          success: false,
          error: 'Chart not found',
        });
      }
      
      res.json({
        success: true,
        chart,
      });
    } catch (error) {
      console.error('Get chart error:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to retrieve chart',
      });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
