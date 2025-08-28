from .gradeCommand import gradeCommand


class getGradeCommand(gradeCommand):
    def __init__(self, student_id: int, course_id: int):
        self.student_id = student_id
        self.course_id = course_id

    def execute(self):
        print(f"Getting grade for student {self.student_id} in course {self.course_id}")
