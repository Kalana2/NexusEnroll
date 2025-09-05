from dataclasses import dataclass
from typing import List


@dataclass
class Class:
    class_id: int
    students: List[int]
