from fastapi import FastAPI
from controllers.schedule_controller import ScheduleController

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
