from src.decorators.base_decorator import BaseSchedule
from src.decorators.highlight_weekends import HighlightWeekendsDecorator
from src.decorators.add_holidays import AddHolidaysDecorator
from supabase import Client, create_client


SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class ScheduleService:
    """Handles schedule building and decoration."""

    def get_student_schedule(self, student_id, semester="2025-Fall"):
        # want to replace with kalana return values
        return BaseSchedule(
            {
                "current": [
                    {
                        "time": "09:00–11:00",
                        "mon": "CS 201",
                        "tue": "CS 205",
                        "wed": "CS 201",
                        "thu": "CS 205",
                        "fri": "ENG 102",
                    },
                    {
                        "time": "11:00–13:00",
                        "mon": "HIST 150",
                        "tue": "",
                        "wed": "",
                        "thu": "",
                        "fri": "",
                    },
                    {
                        "time": "13:00–15:00",
                        "mon": "",
                        "tue": "MATH 310",
                        "wed": "",
                        "thu": "MATH 310",
                        "fri": "",
                    },
                ],
                "past": [
                    {
                        "time": "09:00–11:00",
                        "mon": "",
                        "tue": "MATH 201",
                        "wed": "",
                        "thu": "CS 101",
                        "fri": "",
                    },
                    {
                        "time": "11:00–13:00",
                        "mon": "CS 101",
                        "tue": "",
                        "wed": "ENG 101",
                        "thu": "",
                        "fri": "CS 101",
                    },
                    {
                        "time": "13:00–15:00",
                        "mon": "CS 201",
                        "tue": "MATH 201",
                        "wed": "",
                        "thu": "",
                        "fri": "",
                    },
                ],
            },
        )

    def add_calendar_decorator(self, schedule_view, decorator_type):
        if decorator_type == "highlight_weekends":
            return HighlightWeekendsDecorator(schedule_view)
        elif decorator_type == "add_holidays":
            return AddHolidaysDecorator(schedule_view, holidays=["2025-09-06"])
        return schedule_view

    def generate_calendar(self, student_id, format_type="Weekly"):
        schedule = self.get_student_schedule(student_id, "2025-Fall")
        schedule = HighlightWeekendsDecorator(schedule)
        schedule = AddHolidaysDecorator(schedule, holidays=["2025-09-06"])
        return {"format": format_type, "data": schedule.get_content()}

        def get_table_rows(table_name: str, columns: str = "*"):
            """Return rows from a Supabase table."""
            try:
                resp = supabase.table(table_name).select(columns).execute()
                if getattr(resp, "error", None):
                    raise Exception(
                        resp.error.message
                        if hasattr(resp.error, "message")
                        else resp.error
                    )
                return resp.data
            except Exception as e:
                return {"error": str(e)}

        def get_student_schedule_from_db(student_id, semester):
            """
            Fetch schedule rows for a student and convert to BaseSchedule.
            Expects a 'schedules' table with columns: day, date, classes, student_id, semester.
            """
            try:
                resp = (
                    supabase.table("schedules")
                    .select("day,date,classes")
                    .eq("student_id", student_id)
                    .eq("semester", semester)
                    .order("date", {"ascending": True})
                    .execute()
                )
                if getattr(resp, "error", None):
                    raise Exception(
                        resp.error.message
                        if hasattr(resp.error, "message")
                        else resp.error
                    )
                rows = resp.data or []
                return BaseSchedule(rows)
            except Exception as e:
                # fallback to an empty schedule on error
                return BaseSchedule([])

        def get_students_with_schedules(limit: int = 100):
            """
            Example of linking tables via PostgREST embedding:
            Requires a foreign key relationship so 'schedules' can be embedded into 'students'.
            Returns a list of students each with an embedded 'schedules' list.
            """
            try:
                resp = (
                    supabase.table("students")
                    .select("*, schedules(*)")
                    .limit(limit)
                    .execute()
                )
                if getattr(resp, "error", None):
                    raise Exception(
                        resp.error.message
                        if hasattr(resp.error, "message")
                        else resp.error
                    )
                return resp.data
            except Exception as e:
                return {"error": str(e)}
