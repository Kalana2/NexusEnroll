import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_submit_grades_endpoint():
    response = client.post(
        "/submitGrades/CS101",
        json=[{"studentId": "S001", "grade": "A"}, {"studentId": "S002", "grade": "B"}],
    )
    assert response.status_code == 200
    assert response.json()["status"] == "submitted"


def test_get_grade_endpoint():
    # First submit a grade
    client.post("/submitGrades/CS101", json=[{"studentId": "S003", "grade": "A"}])

    response = client.get("/getGrade/S003")
    assert response.status_code == 200
    assert "CS101" in response.json()["S003"]


def test_approve_grades_endpoint():
    # First submit grades
    client.post("/submitGrades/CS102", json=[{"studentId": "S004", "grade": "B"}])

    response = client.post("/approveGrades/CS102")
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
