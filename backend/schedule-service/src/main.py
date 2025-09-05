from fastapi import FastAPI
from controllers.schedule_controller import ScheduleController
from supabase import create_client, Client

SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Schedule Service", version="1.0")
controller = ScheduleController()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Schedule Service API"}


@app.get("/getStudentSchedule")
def get_student_schedule(student_id: int, semester: str):
    return controller.get_student_schedule(student_id, semester)


@app.get("/addCalendarDecorator")
def add_calendar_decorator(student_id: int, semester: str, decorator_type: str):
    return controller.add_calendar_decorator(student_id, semester, decorator_type)


@app.get("/generateCalendar")
def generate_calendar(student_id: int, format_type: str = "Weekly"):
    return controller.generate_calendar(student_id, format_type)
