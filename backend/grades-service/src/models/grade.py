from dataclasses import dataclass
from supabase import Client, create_client


SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@dataclass
class Grade:
    student_id: int
    course_id: int
    grade: float
    GRADE_TABLE = "grades"

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "course_id": self.course_id,
            "grade": self.grade,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Grade":
        return cls(
            student_id=data["student_id"],
            course_id=data["course_id"],
            grade=data["grade"],
        )

    @classmethod
    def create(cls, grade: "Grade") -> dict:
        res = supabase.table(cls.GRADE_TABLE).insert(grade.to_dict()).execute()
        if getattr(res, "error", None):
            raise RuntimeError(getattr(res, "error", "Unknown error"))
        return res.data[0] if res.data else {}

    @classmethod
    def get_all(cls) -> list:
        res = supabase.table(cls.GRADE_TABLE).select("*").execute()
        if getattr(res, "error", None):
            raise RuntimeError(getattr(res, "error", "Unknown error"))
        return res.data or []

    @classmethod
    def get_by_student(cls, student_id: int) -> list:
        res = (
            supabase.table(cls.GRADE_TABLE)
            .select("*")
            .eq("student_id", student_id)
            .execute()
        )
        if getattr(res, "error", None):
            raise RuntimeError(getattr(res, "error", "Unknown error"))
        return res.data or []

    @classmethod
    def get(cls, student_id: int, course_id: int) -> dict | None:
        res = (
            supabase.table(cls.GRADE_TABLE)
            .select("*")
            .eq("student_id", student_id)
            .eq("course_id", course_id)
            .execute()
        )
        if getattr(res, "error", None):
            raise RuntimeError(getattr(res, "error", "Unknown error"))
        return (res.data or [None])[0]

    @classmethod
    def update(cls, student_id: int, course_id: int, new_grade: float) -> dict:
        res = (
            supabase.table(cls.GRADE_TABLE)
            .update({"grade": new_grade})
            .match({"student_id": student_id, "course_id": course_id})
            .execute()
        )
        if getattr(res, "error", None):
            raise RuntimeError(getattr(res, "error", "Unknown error"))
        return res.data[0] if res.data else {}

    @classmethod
    def delete(cls, student_id: int, course_id: int) -> dict:
        res = (
            supabase.table(cls.GRADE_TABLE)
            .delete()
            .match({"student_id": student_id, "course_id": course_id})
            .execute()
        )
        if getattr(res, "error", None):
            raise RuntimeError(getattr(res, "error", "Unknown error"))
        return res.data[0] if res.data else {}
