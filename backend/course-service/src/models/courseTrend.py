from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseTrend(BaseModel):
    course_id: str
    course_name: str
    popularity_score: float
    enrollment_rate: float
    waitlist_count: int
    trend_direction: str  # "up", "down", "stable"
    last_updated: datetime

    class Config:
        schema_extra = {
            "example": {
                "course_id": "CS101",
                "course_name": "Introduction to Computer Science",
                "popularity_score": 8.5,
                "enrollment_rate": 0.85,
                "waitlist_count": 15,
                "trend_direction": "up",
                "last_updated": "2023-10-15T14:30:00Z",
            }
        }
