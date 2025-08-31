from dataclasses import dataclass
from typing import List


@dataclass
class Course:
    course_number: int
    name: str
    semester: int
    description: str
    instructor: str
    capacity: int
    credits: int
    is_critical: bool
    students: List[str]
