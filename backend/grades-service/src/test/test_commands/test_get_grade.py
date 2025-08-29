import pytest
from commands.getGradeCommand import GetGradeCommand
from services.gradeService import GradeService


def test_get_grade_command():
    service = GradeService()
    student_id = "S001"

    # First submit some grades
    service.submit_grades("CS101", [{"studentId": student_id, "grade": "A"}])

    cmd = GetGradeCommand(service, student_id)
    result = cmd.execute()

    assert student_id in result
    assert result[student_id]["CS101"] == "A"
