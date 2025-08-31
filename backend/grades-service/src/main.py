from fastapi import FastAPI
from commands.submitGradesCommand import SubmitGradesCommand
from commands.getGradeCommand import GetGradeCommand
from commands.approveGradesCommand import ApproveGradesCommand
from commands.processGradesCommand import ProcessGradesCommand
from handlers.commandProcessor import CommandProcessor
from services.gradeService import GradeService
from typing import Any

app = FastAPI(title="Grades Service with Command Pattern")

# Singletons
grade_service = GradeService()
processor = CommandProcessor()


@app.get("/")
def read_root() -> Any:
    return {"message": "Welcome to the Grades Service!"}


@app.post("/submitGrades/{courseId}")
def submit_grades(course_id: str, grade_batch: list[dict]):
    cmd = SubmitGradesCommand(course_id, grade_batch)
    return processor.process(cmd)


@app.get("/getGrades/{student_id}")
def get_grades(student_id: str):
    cmd = GetGradeCommand(student_id, grade_service)
    return processor.process(cmd)


@app.post("/approveGrades/{courseId}")
def approve_grades(course_id: str):
    cmd = ApproveGradesCommand(grade_service, course_id)
    return processor.process(cmd)


@app.post("/processGrades/{courseId}")
def process_grades(course_id: str):
    cmd = ProcessGradesCommand(grade_service, course_id)
    return processor.process(cmd)
