from dataclasses import dataclass
from typing import List


@dataclass
class Prerequisite:
    prerequisite_id: int
    course_number: List[int]
    prerequisites: List[int]
