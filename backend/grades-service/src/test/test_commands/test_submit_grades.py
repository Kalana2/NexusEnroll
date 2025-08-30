import pytest
from commands.submitGradesCommand import SubmitGradesCommand
from services.gradeService import GradeService


def test_submit_grades_command():
    service = GradeService()
    course_id = "CS101"
    grade_batch = [
        {"studentId": "S001", "grade": "A"},
        {"studentId": "S002", "grade": "B"},
    ]

    cmd = SubmitGradesCommand(service, course_id, grade_batch)
    result: dict = cmd.execute()

    assert result["status"] == "submitted"
    assert len(result["grades"]) == 2
