from fastapi import FastAPI
from commands.submitGradesCommand import SubmitGradesCommand
from commands.getGradeCommand import GetGradeCommand

from commands.approveGrades import ApproveGradesCommand
from commands.processGradesCommand import ProcessGradesCommand
from handlers.commandProcessor import CommandProcessor
from services.gradeService import GradeService

app = FastAPI(title="Grades Service with Command Pattern")

# Singletons
grade_service = GradeService()
processor = CommandProcessor()


@app.post("/submitGrades/{courseId}")
def submit_grades(course_id: str, grade_batch: list[dict]):
    cmd = SubmitGradesCommand(grade_service, course_id, grade_batch)
    return processor.process(cmd)


@app.get("/getGrade/{student_id}")
def get_grades(student_id: int):
    cmd = GetGradeCommand(student_id, student_id)
    return processor.process(cmd)


@app.post("/approveGrades/{courseId}")
def approve_grades(course_id: int):
    cmd = ApproveGradesCommand(grade_service, course_id)
    return processor.process(cmd)
