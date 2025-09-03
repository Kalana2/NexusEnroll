from typing import List
from src.models import Course

class CourseServiceClient:
    def list_courses(self, dept: str) -> List[Course]:
        data = [
            Course("CS101","Intro to CS","Business",100,93,"Dr. Perera"),
            Course("CS102","Data Structures","CS",180,160,"Dr. Silva"),
            Course("MKT210","Digital Marketing","Business",120,119,"Dr. Fernando"),
            Course("FIN300","Financial Analytics","Business",60,48,"Dr. Jayasena"),
        ]
        return [c for c in data if c.dept == dept]
