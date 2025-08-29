import pytest
from services.gradeService import GradeService


def test_submit_grades():
    service = GradeService()
    result = service.submit_grades(
        "CS101",
        [{"studentId": "S001", "grade": "A"}, {"studentId": "S002", "grade": "B"}],
    )

    assert result["status"] == "submitted"
    assert len(service.get_grades("S001")) > 0


def test_approve_grades():
    service = GradeService()
    service.submit_grades("CS101", [{"studentId": "S001", "grade": "A"}])

    result = service.approve_grades("CS101")
    assert result["status"] == "approved"


def test_get_grades():
    service = GradeService()
    service.submit_grades("CS101", [{"studentId": "S001", "grade": "A"}])
    service.approve_grades("CS101")

    grades = service.get_grades("S001")
    assert grades["CS101"]["grade"] == "A"
    assert grades["CS101"]["status"] == "approved"
