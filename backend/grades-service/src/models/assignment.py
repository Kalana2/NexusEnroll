from dataclasses import dataclass


@dataclass
class Assignment:
    assignment_id: str
    course_id: str
    title: str
    max_score: int
