from .gradeCommand import GradeCommand


class GetGradeCommand(GradeCommand):
    def __init__(self, student_id, grade_service):
        self.student_id = student_id
        self.grade_service = grade_service

    def execute(self):
        print(f"Getting grades for student {self.student_id}")
        return self.grade_service.getGrades(self.student_id)
