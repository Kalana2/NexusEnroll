from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import time


class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class Schedule(BaseModel):
    days: List[DayOfWeek]
    start_time: time
    end_time: time
    location: str


class Course(BaseModel):
    id: str = Field(..., description="Unique course identifier")
    name: str = Field(..., description="Course name")
    description: str = Field(..., description="Course description")
    department: str = Field(..., description="Department offering the course")
    code: str = Field(..., description="Course code")
    instructor: str = Field(..., description="Instructor name")
    credits: int = Field(..., description="Number of credits")
    total_capacity: int = Field(..., description="Total available seats")
    current_enrollment: int = Field(
        ..., description="Current number of enrolled students"
    )
    schedule: Optional[Schedule] = Field(None, description="Course schedule")
    prerequisites: Optional[List[str]] = Field(
        [], description="List of prerequisite course IDs"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": "CS101",
                "name": "Introduction to Computer Science",
                "description": "Fundamental concepts of computer science",
                "department": "Computer Science",
                "code": "CS101",
                "instructor": "Dr. Jane Smith",
                "credits": 3,
                "total_capacity": 100,
                "current_enrollment": 85,
                "prerequisites": [],
            }
        }


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    instructor: Optional[str] = None
    total_capacity: Optional[int] = None
    schedule: Optional[Schedule] = None

    class Config:
        schema_extra = {
            "example": {"instructor": "Dr. John Doe", "total_capacity": 120}
        }
