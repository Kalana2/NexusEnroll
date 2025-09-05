from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Any

from supabase import Client, create_client


SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@dataclass
class Prerequisite:
    prerequisite_id: Optional[int]
    course_number: List[int]
    prerequisites: List[int]
    _TABLE = "prerequisites"

    @classmethod
    def _row_to_prereq(cls, row: dict) -> "Prerequisite":
        # Accept either "prerequisite_id" or "id" as primary key returned by Supabase
        pid = (
            row.get("prerequisite_id")
            if row.get("prerequisite_id") is not None
            else row.get("id")
        )
        return cls(
            prerequisite_id=pid,
            course_number=row.get("course_number", []) or [],
            prerequisites=row.get("prerequisites", []) or [],
        )

    @classmethod
    def get_all_prerequisites(cls) -> List["Prerequisite"]:
        res = supabase.table(cls._TABLE).select("*").execute()
        if getattr(res, "error", None):
            raise RuntimeError(f"Supabase error: {getattr(res, 'error', None)}")
        data = getattr(res, "data", []) or []
        return [cls._row_to_prereq(r) for r in data]

    @classmethod
    def get_prerequisite_by_id(cls, prerequisite_id: int) -> Optional["Prerequisite"]:
        res = (
            supabase.table(cls._TABLE)
            .select("*")
            .eq("prerequisite_id", prerequisite_id)
            .single()
            .execute()
        )
        if getattr(res, "error", None):
            # If not found, Supabase may return an error; return None in that case
            return None
        row = getattr(res, "data", None)
        return cls._row_to_prereq(row) if row else None

    @classmethod
    def insert_prerequisite(cls, pr: "Prerequisite") -> "Prerequisite":
        payload: dict[str, Any] = {
            "prerequisite_id": pr.prerequisite_id,
            "course_number": pr.course_number,
            "prerequisites": pr.prerequisites,
        }
        # call execute() directly (avoids static type issue with .select on the builder)
        res = supabase.table(cls._TABLE).insert(payload).execute()
        if getattr(res, "error", None):
            raise RuntimeError(f"Supabase error: {getattr(res, 'error', None)}")
        data = getattr(res, "data", []) or []
        return cls._row_to_prereq(data[0])

    @classmethod
    def update_prerequisite(
        cls, prerequisite_id: int, **fields
    ) -> Optional["Prerequisite"]:
        if not fields:
            return cls.get_prerequisite_by_id(prerequisite_id)
        # call execute() directly (avoids static type issue with .select on the builder)
        res = (
            supabase.table(cls._TABLE)
            .update(fields)
            .eq("prerequisite_id", prerequisite_id)
            .execute()
        )
        if getattr(res, "error", None):
            raise RuntimeError(f"Supabase error: {getattr(res, 'error', None)}")
        data = getattr(res, "data", []) or []
        return cls._row_to_prereq(data[0]) if data else None

    @classmethod
    def delete_prerequisite(cls, prerequisite_id: int) -> bool:
        res = (
            supabase.table(cls._TABLE)
            .delete()
            .eq("prerequisite_id", prerequisite_id)
            .execute()
        )
        if getattr(res, "error", None):
            raise RuntimeError(f"Supabase error: {getattr(res, 'error', None)}")
        # If delete succeeded, Supabase typically returns the deleted rows; treat success if any row returned
        data = getattr(res, "data", []) or []
        return len(data) > 0
