from .gradeCommand import GradeCommand


class ProcessGradesCommand(GradeCommand):
    def __init__(self, grade_service, course_id):
        self.grade_service = grade_service
        self.course_id = course_id

    def execute(self):
        return self.grade_service.approve_grades(self.course_id)
