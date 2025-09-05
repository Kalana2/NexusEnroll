from dataclasses import dataclass
from supabase import Client, create_client


SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@dataclass
class Assignment:
    assignment_id: str
    course_id: str
    title: str
    max_score: int
    TABLE_NAME = "assignments"

    @classmethod
    def _from_row(cls, row: dict) -> "Assignment":
        return cls(
            assignment_id=str(row.get("assignment_id") or row.get("id") or ""),
            course_id=str(row.get("course_id") or ""),
            title=str(row.get("title") or ""),
            max_score=int(row.get("max_score") or 0),
        )

    @classmethod
    def get_all(cls) -> list["Assignment"]:
        resp = supabase.table(cls.TABLE_NAME).select("*").execute()
        data = getattr(resp, "data", None) or (
            resp.get("data") if isinstance(resp, dict) else None
        )
        if not data:
            return []
        return [cls._from_row(r) for r in data]

    @classmethod
    def get_by_id(cls, assignment_id: str) -> "Assignment | None":
        resp = (
            supabase.table(cls.TABLE_NAME)
            .select("*")
            .eq("assignment_id", assignment_id)
            .single()
            .execute()
        )
        data = getattr(resp, "data", None) or (
            resp.get("data") if isinstance(resp, dict) else None
        )
        if not data:
            return None
        return cls._from_row(data)

    def insert(self) -> bool:
        payload = {
            "assignment_id": self.assignment_id,
            "course_id": self.course_id,
            "title": self.title,
            "max_score": self.max_score,
        }
        resp = supabase.table(self.TABLE_NAME).insert(payload).execute()
        err = getattr(resp, "error", None) or (
            resp.get("error") if isinstance(resp, dict) else None
        )
        return err is None

    def update(self) -> bool:
        payload = {
            "course_id": self.course_id,
            "title": self.title,
            "max_score": self.max_score,
        }
        resp = (
            supabase.table(self.TABLE_NAME)
            .update(payload)
            .eq("assignment_id", self.assignment_id)
            .execute()
        )
        err = getattr(resp, "error", None) or (
            resp.get("error") if isinstance(resp, dict) else None
        )
        return err is None

    @classmethod
    def delete_by_id(cls, assignment_id: str) -> bool:
        resp = (
            supabase.table(cls.TABLE_NAME)
            .delete()
            .eq("assignment_id", assignment_id)
            .execute()
        )
        err = getattr(resp, "error", None) or (
            resp.get("error") if isinstance(resp, dict) else None
        )
        return err is None
