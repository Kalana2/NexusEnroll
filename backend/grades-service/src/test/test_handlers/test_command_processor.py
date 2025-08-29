import pytest
from handlers.commandProcessor import CommandProcessor
from commands.submitGradesCommand import SubmitGradesCommand
from services.gradeService import GradeService


def test_command_processor():
    processor = CommandProcessor()
    service = GradeService()

    cmd = SubmitGradesCommand(service, "CS101", [{"studentId": "S001", "grade": "A"}])
    result = processor.process(cmd)

    assert result["status"] == "submitted"
