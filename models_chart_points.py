"""
Enhanced models with all required astrological points.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Ascendant(BaseModel):
    """Model for Ascendant (Rising Sign) information."""
    
    sign: str = Field(..., description="Rising sign")
    degree: float = Field(..., ge=0, lt=360, description="Degree position")
    exactDegree: str = Field(..., description="Exact degree in format 'XX°XX'XX\"'")
    

class MoonPhase(BaseModel):
    """Model for Moon phase information."""
    
    phaseName: str = Field(..., description="Name of the moon phase")
    illumination: float = Field(..., ge=0, le=100, description="Percentage of moon illuminated")
    isVoidOfCourse: bool = Field(False, description="Whether Moon is void of course")
    nextAspect: Optional[str] = Field(None, description="Next major aspect the Moon will make")


class ChartRuler(BaseModel):
    """Model for chart ruler information."""
    
    planet: str = Field(..., description="Chart ruling planet")
    sign: str = Field(..., description="Sign the chart ruler is in")
    house: int = Field(..., ge=1, le=12, description="House the chart ruler is in")
    degree: float = Field(..., ge=0, lt=360, description="Degree position")
    exactDegree: str = Field(..., description="Exact degree in format 'XX°XX'XX\"'")
    retrograde: bool = Field(False, description="Whether chart ruler is retrograde")


class HouseInfo(BaseModel):
    """Model for individual house information in Whole Sign system."""
    
    house: int = Field(..., ge=1, le=12, description="House number")
    sign: str = Field(..., description="Sign on house cusp (same sign throughout in Whole Sign)")
    ruler: str = Field(..., description="Traditional ruler of this house sign")
    planets: List[str] = Field(default_factory=list, description="Planets located in this house")


class ChartAngle(BaseModel):
    """Model for major chart angles (MC, IC, DC)."""
    
    sign: str = Field(..., description="Zodiac sign")
    degree: float = Field(..., ge=0, lt=360, description="Degree position")
    exactDegree: str = Field(..., description="Exact degree in format 'XX°XX'XX\"'")
    
    class Config:
        json_schema_extra = {
            "example": {
                "sign": "Taurus",
                "degree": 15.3,
                "exactDegree": "15°18'00\""
            }
        }


class PlacementInfo(BaseModel):
    """Model for individual planet placement information."""
    
    planet: str = Field(..., description="Planet or celestial body name")
    sign: str = Field(..., description="Zodiac sign")
    house: int = Field(..., ge=1, le=12, description="House position")
    degree: float = Field(..., ge=0, lt=360, description="Degree position")
    exactDegree: str = Field(..., description="Exact degree in format 'XX°XX'XX\"'")
    retrograde: bool = Field(False, description="Retrograde status")
    houseRuler: Optional[str] = Field(None, description="Traditional ruler of the house this planet occupies")


class CompleteChartResponse(BaseModel):
    """Complete astrology chart response with all required points."""
    
    # Basic Chart Points
    risingSign: str = Field(..., description="Rising sign (Ascendant)")
    sunSign: str = Field(..., description="Sun sign") 
    moonSign: str = Field(..., description="Moon sign")
    
    # Detailed Ascendant Information
    ascendant: Ascendant = Field(..., description="Detailed Ascendant (Rising Sign) information")
    
    # Chart Angles
    midheaven: ChartAngle = Field(..., description="Midheaven (MC) position")
    descendant: ChartAngle = Field(..., description="Descendant (DC) position")
    imumCoeli: ChartAngle = Field(..., description="Imum Coeli (IC) position")
    
    # All Planetary Placements
    placements: List[PlacementInfo] = Field(..., description="All planetary placements")
    
    # House Information (Whole Sign System)
    houses: List[HouseInfo] = Field(..., description="Complete house breakdown with rulers and planet placements")
    
    # Chart Ruler
    chartRuler: ChartRuler = Field(..., description="Chart ruler based on Rising sign")
    
    # Moon Phase Information
    moonPhase: MoonPhase = Field(..., description="Current moon phase and void of course status")
    
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
                    },
                    {
                        "planet": "North Node",
                        "sign": "Leo",
                        "house": 1,
                        "degree": 22.8,
                        "retrograde": False
                    },
                    {
                        "planet": "South Node",
                        "sign": "Aquarius",
                        "house": 7,
                        "degree": 22.8,
                        "retrograde": False
                    }
                ],
                "houseSystem": "W",
                "generatedAt": "2025-01-26T12:00:00"
            }
        }