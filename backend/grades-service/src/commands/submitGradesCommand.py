from .gradeCommand import GradeCommand


class SubmitGradesCommand(GradeCommand):
    def __init__(self, course_id, grade_batch):
        self.course_id = course_id
        self.grade_batch = grade_batch

    def execute(self):
        print(
            f"Submitting grades for course {self.course_id} with batch {self.grade_batch}"
        )
        return (self.course_id, self.grade_batch)
