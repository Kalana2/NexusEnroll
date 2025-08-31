from dataclasses import dataclass


@dataclass
class Grade:
    student_id: int
    course_id: int
    grade: float
