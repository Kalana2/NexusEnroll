from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import time

from supabase import Client, create_client
from typing import List, Optional, Dict, Any
from pydantic import ValidationError

SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "courses"


def _handle_response(response) -> Optional[Any]:
    # supabase-python returns an object with .data and .error on .execute()
    if getattr(response, "error", None):
        raise RuntimeError(f"Supabase error: {response.error}")
    return getattr(response, "data", None)


def list_courses() -> List[Course]:
    """Return all courses from the courses table."""
    res = supabase.table(TABLE_NAME).select("*").execute()
    data = _handle_response(res)
    return [Course(**item) for item in (data or [])]


def get_course(course_id: str) -> Optional[Course]:
    """Return a single course by id or None if not found."""
    res = supabase.table(TABLE_NAME).select("*").eq("id", course_id).limit(1).execute()
    data = _handle_response(res)
    if not data:
        return None
    try:
        return Course(**data[0])
    except ValidationError as e:
        raise RuntimeError(f"Data validation failed: {e}")


def create_course(course: Course) -> Course:
    """Insert a new course and return the created record."""
    payload = course.dict()
    res = supabase.table(TABLE_NAME).insert(payload).execute()
    data = _handle_response(res)
    if not data:
        raise RuntimeError("Failed to create course")
    try:
        return Course(**data[0])
    except ValidationError as e:
        raise RuntimeError(f"Created data validation failed: {e}")


def update_course(course_id: str, updates: CourseUpdate) -> Optional[Course]:
    """Update fields of a course and return the updated record."""
    payload = updates.dict(exclude_unset=True)
    if not payload:
        return get_course(course_id)
    res = supabase.table(TABLE_NAME).update(payload).eq("id", course_id).execute()
    data = _handle_response(res)
    if not data:
        return None
    try:
        return Course(**data[0])
    except ValidationError as e:
        raise RuntimeError(f"Updated data validation failed: {e}")


def delete_course(course_id: str) -> bool:
    """Delete a course by id. Returns True if a row was deleted."""
    res = supabase.table(TABLE_NAME).delete().eq("id", course_id).execute()
    data = _handle_response(res)
    return bool(data)


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
