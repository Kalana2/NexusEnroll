from .gradeCommand import GradeCommand


class SubmitGradesCommand(GradeCommand):
    def __init__(self, grade_service, course_id, grade_batch):
        self.grade_service = grade_service
        self.course_id = course_id
        self.grade_batch = grade_batch

    def execute(self):
        return self.grade_service.submit_grades(self.course_id, self.grade_batch)
