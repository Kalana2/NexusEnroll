from .gradeCommand import GradeCommand


class ApproveGradesCommand(GradeCommand):
    def __init__(self, grade_service, course_id: int):
        self.grade_service = grade_service
        self.course_id = course_id

    def execute(self):
        return self.grade_service.approveGrades(self.course_id)
