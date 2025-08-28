from .gradeCommand import gradeCommand


class submitGradeCommand(gradeCommand):
    def __init__(self, student_id: int, course_id: int, grade: float):
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade

    def execute(self):
        print(
            f"Submitting grade {self.grade} for student {self.student_id} in course {self.course_id}"
        )
