from pydantic import BaseModel
from typing import Optional
from datetime import datetimefrom
from supabase import Client, create_client


SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "course_trends"


def get_all_course_trends():
    resp = supabase.table(TABLE_NAME).select("*").execute()
    if getattr(resp, "error", None):
        raise Exception(str(resp.error))
    return resp.data


def get_course_trend(course_id: str):
    resp = (
        supabase.table(TABLE_NAME)
        .select("*")
        .eq("course_id", course_id)
        .single()
        .execute()
    )
    if getattr(resp, "error", None):
        raise Exception(str(resp.error))
    return resp.data


def create_course_trend(trend: "CourseTrend"):
    payload = trend.dict()
    resp = supabase.table(TABLE_NAME).insert(payload).execute()
    if getattr(resp, "error", None):
        raise Exception(str(resp.error))
    return resp.data


def update_course_trend(course_id: str, updates: dict):
    resp = (
        supabase.table(TABLE_NAME).update(updates).eq("course_id", course_id).execute()
    )
    if getattr(resp, "error", None):
        raise Exception(str(resp.error))
    return resp.data


def delete_course_trend(course_id: str):
    resp = supabase.table(TABLE_NAME).delete().eq("course_id", course_id).execute()
    if getattr(resp, "error", None):
        raise Exception(str(resp.error))
    return resp.data


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
