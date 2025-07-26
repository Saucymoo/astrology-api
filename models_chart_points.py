"""
Enhanced models with all required astrological points.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChartAngle(BaseModel):
    """Model for major chart angles (MC, IC, DC)."""
    
    sign: str = Field(..., description="Zodiac sign")
    degree: float = Field(..., ge=0, lt=360, description="Degree position")
    
    class Config:
        json_schema_extra = {
            "example": {
                "sign": "Taurus",
                "degree": 15.3
            }
        }


class PlacementInfo(BaseModel):
    """Model for individual planet placement information."""
    
    planet: str = Field(..., description="Planet or celestial body name")
    sign: str = Field(..., description="Zodiac sign")
    house: int = Field(..., ge=1, le=12, description="House position")
    degree: float = Field(..., ge=0, lt=360, description="Degree position")
    retrograde: bool = Field(False, description="Retrograde status")


class CompleteChartResponse(BaseModel):
    """Complete astrology chart response with all required points."""
    
    # Basic Chart Points
    risingSign: str = Field(..., description="Rising sign (Ascendant)")
    sunSign: str = Field(..., description="Sun sign")
    moonSign: str = Field(..., description="Moon sign")
    
    # Chart Angles
    midheaven: ChartAngle = Field(..., description="Midheaven (MC) position")
    descendant: ChartAngle = Field(..., description="Descendant (DC) position")
    imumCoeli: ChartAngle = Field(..., description="Imum Coeli (IC) position")
    
    # All Planetary Placements
    placements: List[PlacementInfo] = Field(..., description="All planetary placements")
    
    # Generation metadata
    houseSystem: str = Field("W", description="House system used (W = Whole Sign)")
    generatedAt: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "risingSign": "Leo",
                "sunSign": "Gemini",
                "moonSign": "Pisces",
                "midheaven": {
                    "sign": "Taurus",
                    "degree": 15.3
                },
                "descendant": {
                    "sign": "Aquarius", 
                    "degree": 15.3
                },
                "imumCoeli": {
                    "sign": "Scorpio",
                    "degree": 15.3
                },
                "placements": [
                    {
                        "planet": "Sun",
                        "sign": "Gemini",
                        "house": 11,
                        "degree": 24.5,
                        "retrograde": False
                    },
                    {
                        "planet": "Moon",
                        "sign": "Pisces",
                        "house": 8,
                        "degree": 15.2,
                        "retrograde": False
                    },
                    {
                        "planet": "Mercury",
                        "sign": "Gemini",
                        "house": 10,
                        "degree": 18.7,
                        "retrograde": True
                    },
                    {
                        "planet": "Venus",
                        "sign": "Cancer",
                        "house": 12,
                        "degree": 5.1,
                        "retrograde": False
                    },
                    {
                        "planet": "Mars",
                        "sign": "Aries",
                        "house": 9,
                        "degree": 28.9,
                        "retrograde": False
                    },
                    {
                        "planet": "Jupiter",
                        "sign": "Sagittarius",
                        "house": 5,
                        "degree": 12.4,
                        "retrograde": False
                    },
                    {
                        "planet": "Saturn",
                        "sign": "Capricorn",
                        "house": 6,
                        "degree": 22.8,
                        "retrograde": True
                    },
                    {
                        "planet": "Uranus",
                        "sign": "Aquarius",
                        "house": 7,
                        "degree": 8.2,
                        "retrograde": False
                    },
                    {
                        "planet": "Neptune",
                        "sign": "Pisces",
                        "house": 8,
                        "degree": 16.5,
                        "retrograde": True
                    },
                    {
                        "planet": "Pluto",
                        "sign": "Scorpio",
                        "house": 4,
                        "degree": 9.7,
                        "retrograde": False
                    },
                    {
                        "planet": "Chiron",
                        "sign": "Virgo",
                        "house": 2,
                        "degree": 14.3,
                        "retrograde": False
                    }
                ],
                "houseSystem": "W",
                "generatedAt": "2025-01-26T12:00:00"
            }
        }