import pytest
from fastapi.testclient import TestClient
from main import app, gradeService, processor


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def mock_grade_service():
    return gradeService


@pytest.fixture
def mock_processor():
    return processor
