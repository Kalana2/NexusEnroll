from dataclasses import dataclass

@dataclass
class Course:
    id: str
    name: str
    dept: str
    capacity: int
    enrolled: int
    instructor: str
