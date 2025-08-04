"""
Pydantic models for the astrology API.

These models define the data structures for requests and responses,
ensuring type safety and validation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re


class BirthInfoRequest(BaseModel):
    """Request model for birth information."""

    name: str = Field(...,
                      min_length=1,
                      max_length=100,
                      description="Full name")
    date: str = Field(
        ...,
        description="Birth date in YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY format"
    )
    time: str = Field(...,
                      pattern=r'^\d{2}:\d{2}$',
                      description="Birth time in HH:MM format (24-hour)")
    location: str = Field(...,
                          min_length=1,
                          max_length=200,
                          description="Birth location (city, state, country)")
    latitude: Optional[float] = Field(None,
                                      ge=-90,
                                      le=90,
                                      description="Latitude coordinate")
    longitude: Optional[float] = Field(None,
                                       ge=-180,
                                       le=180,
                                       description="Longitude coordinate")
    timezone: Optional[float] = Field(None,
                                      ge=-12,
                                      le=14,
                                      description="Timezone offset in hours")

    @validator('date')
    def validate_date(cls, v):
        """Validate date format and ensure it's a valid date."""
        # Try multiple date formats
        formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']

        for fmt in formats:
            try:
                parsed_date = datetime.strptime(v, fmt)
                # Return in standardized ISO format
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue

        raise ValueError(
            'Date must be in YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY format and be a valid date'
        )

    @validator('time')
    def validate_time(cls, v):
        """Validate time format and ensure it's a valid time."""
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError(
                'Time must be in HH:MM format (24-hour) and be a valid time')

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "date": "1990-06-15",
                "time": "14:30",
                "location": "New York, NY, USA",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "timezone": -5
            }
        }


class Planet(BaseModel):
    """Model for planetary positions."""

    name: str = Field(..., description="Planet name")
    sign: str = Field(..., description="Zodiac sign")
    sign_num: int = Field(..., ge=1, le=12, description="Sign number (1-12)")
    degree: float = Field(..., ge=0, lt=360, description="Degree within sign")
    house: int = Field(..., ge=1, le=12, description="House position")
    retro: Optional[bool] = Field(False, description="Retrograde status")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sun",
                "sign": "Gemini",
                "sign_num": 3,
                "degree": 24.5,
                "house": 10,
                "retro": False
            }
        }


class House(BaseModel):
    """Model for astrological houses."""

    house: int = Field(..., ge=1, le=12, description="House number")
    sign: str = Field(..., description="Sign on house cusp")
    sign_num: int = Field(..., ge=1, le=12, description="Sign number (1-12)")
    degree: float = Field(...,
                          ge=0,
                          lt=360,
                          description="Degree of house cusp")

    class Config:
        json_schema_extra = {
            "example": {
                "house": 1,
                "sign": "Leo",
                "sign_num": 5,
                "degree": 15.3
            }
        }


class Ascendant(BaseModel):
    """Model for the Ascendant (Rising Sign)."""

    sign: str = Field(..., description="Ascending zodiac sign")
    degree: float = Field(..., ge=0, lt=360, description="Degree of Ascendant")

    class Config:
        json_schema_extra = {"example": {"sign": "Leo", "degree": 15.3}}


class Midheaven(BaseModel):
    """Model for the Midheaven (MC)."""

    sign: str = Field(..., description="Midheaven zodiac sign")
    degree: float = Field(..., ge=0, lt=360, description="Degree of Midheaven")

    class Config:
        json_schema_extra = {"example": {"sign": "Taurus", "degree": 21.4}}


class AstrologyResponse(BaseModel):
    """Response model for astrology chart data."""

    success: bool = Field(True, description="Request success status")
    name: str = Field(..., description="Person's name")
    birth_info: BirthInfoRequest = Field(
        ..., description="Original birth information")
    planets: List[Planet] = Field(..., description="Planetary positions")
    houses: List[House] = Field(..., description="House cusps")
    ascendant: Ascendant = Field(..., description="Rising sign information")
    midheaven: Midheaven = Field(...,
                                 description="Midheaven (MC) sign and degree")

    generated_at: datetime = Field(default_factory=datetime.now,
                                   description="Chart generation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "success":
                True,
                "name":
                "John Doe",
                "birth_info": {
                    "name": "John Doe",
                    "date": "1990-06-15",
                    "time": "14:30",
                    "location": "New York, NY, USA",
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "timezone": -5
                },
                "planets": [{
                    "name": "Sun",
                    "sign": "Gemini",
                    "sign_num": 3,
                    "degree": 24.5,
                    "house": 10,
                    "retro": False
                }],
                "houses": [{
                    "house": 1,
                    "sign": "Leo",
                    "sign_num": 5,
                    "degree": 15.3
                }],
                "ascendant": {
                    "sign": "Leo",
                    "degree": 15.3
                },
                "midheaven": {
                    "sign": "Taurus",
                    "degree": 21.4
                },
                "generated_at":
                "2025-01-26T12:00:00"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""

    success: bool = Field(False, description="Request success status")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None,
                                  description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now,
                                description="Error timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Invalid birth date format",
                "detail": "Date must be in YYYY-MM-DD format",
                "timestamp": "2025-01-26T12:00:00"
            }
        }


class CoordinatesResponse(BaseModel):
    """Response model for geocoding coordinates."""

    location: str = Field(..., description="Original location query")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    timezone: float = Field(..., description="Estimated timezone offset")
    display_name: Optional[str] = Field(None, description="Full location name")

    class Config:
        json_schema_extra = {
            "example": {
                "location": "New York, NY, USA",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "timezone": -5,
                "display_name": "New York, New York, United States"
            }
        }
