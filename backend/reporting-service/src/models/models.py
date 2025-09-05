from pydantic import BaseModel
from supabase import Client, create_client
from typing import List, Optional, Dict, Any
from datetime import datetime


SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class ReportRequest(BaseModel):
    report_type: str
    format: str


class Report(BaseModel):
    id: Optional[int]
    title: Optional[str]
    content: Optional[str]
    report_type: str
    format: str
    user_id: Optional[int]
    created_at: Optional[datetime]


class User(BaseModel):
    id: Optional[int]
    email: Optional[str]
    full_name: Optional[str]


def _unwrap_response(res: Any) -> List[Dict[str, Any]]:
    # supabase-py may return an object with .data or a dict with "data"
    if hasattr(res, "data"):
        return res.data or []
    if isinstance(res, dict):
        return res.get("data", []) or []
    return []


def fetch_reports(
    report_type: Optional[str] = None, format_: Optional[str] = None
) -> List[Report]:
    query = supabase.table("reports").select("*")
    if report_type:
        query = query.eq("report_type", report_type)
    if format_:
        query = query.eq("format", format_)
    res = query.execute()
    rows = _unwrap_response(res)
    return [Report(**r) for r in rows]


def get_report_by_id(report_id: int) -> Optional[Report]:
    res = supabase.table("reports").select("*").eq("id", report_id).limit(1).execute()
    rows = _unwrap_response(res)
    return Report(**rows[0]) if rows else None


def create_report(
    request: ReportRequest,
    title: str,
    content: Optional[str] = None,
    user_id: Optional[int] = None,
) -> Report:
    payload = {
        "title": title,
        "content": content,
        "report_type": request.report_type,
        "format": request.format,
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
    }
    res = supabase.table("reports").insert(payload).execute()
    rows = _unwrap_response(res)
    return Report(**rows[0])


def update_report(report_id: int, changes: Dict[str, Any]) -> Optional[Report]:
    res = supabase.table("reports").update(changes).eq("id", report_id).execute()
    rows = _unwrap_response(res)
    return Report(**rows[0]) if rows else None


def delete_report(report_id: int) -> bool:
    res = supabase.table("reports").delete().eq("id", report_id).execute()
    rows = _unwrap_response(res)
    return bool(rows)


def fetch_users() -> List[User]:
    res = supabase.table("users").select("*").execute()
    rows = _unwrap_response(res)
    return [User(**r) for r in rows]


def get_user_by_id(user_id: int) -> Optional[User]:
    res = supabase.table("users").select("*").eq("id", user_id).limit(1).execute()
    rows = _unwrap_response(res)
    return User(**rows[0]) if rows else None
