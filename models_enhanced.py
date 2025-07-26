"""
Enhanced models for the astrology API with user's preferred response format.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PlacementInfo(BaseModel):
    """Model for individual planet placement information."""
    
    planet: str = Field(..., description="Planet name")
    sign: str = Field(..., description="Zodiac sign")
    house: int = Field(..., ge=1, le=12, description="House position")
    degree: float = Field(..., ge=0, lt=360, description="Degree position")
    retrograde: bool = Field(False, description="Retrograde status")


class ChartResponse(BaseModel):
    """User's preferred response format for astrology charts."""
    
    risingSign: str = Field(..., description="Rising sign (Ascendant)")
    sunSign: str = Field(..., description="Sun sign")
    moonSign: str = Field(..., description="Moon sign")
    midheaven: str = Field(..., description="Midheaven sign (10th house cusp)")
    placements: List[PlacementInfo] = Field(..., description="All planetary placements")
    
    class Config:
        json_schema_extra = {
            "example": {
                "risingSign": "Leo",
                "sunSign": "Gemini",
                "moonSign": "Pisces",
                "midheaven": "Taurus",
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
                    }
                ]
            }
        }