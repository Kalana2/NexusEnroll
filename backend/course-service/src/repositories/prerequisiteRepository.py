from typing import List


class PrerequisiteRepository:
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For this example, we'll use a simple in-memory storage
        self.prerequisites = {"CS201": ["CS101"]}  # CS201 requires CS101

    def find_prerequisites(self, course_id: str) -> List[str]:
        """Find all prerequisites for a course"""
        return self.prerequisites.get(course_id, [])

    def find_prerequisite(self, course_id: str, prerequisite_id: str) -> bool:
        """Check if a specific prerequisite exists"""
        return prerequisite_id in self.prerequisites.get(course_id, [])

    def add_prerequisite(self, course_id: str, prerequisite_id: str) -> bool:
        """Add a prerequisite to a course"""
        if course_id not in self.prerequisites:
            self.prerequisites[course_id] = []

        if prerequisite_id not in self.prerequisites[course_id]:
            self.prerequisites[course_id].append(prerequisite_id)

        return True

    def remove_prerequisite(self, course_id: str, prerequisite_id: str) -> bool:
        """Remove a prerequisite from a course"""
        if (
            course_id in self.prerequisites
            and prerequisite_id in self.prerequisites[course_id]
        ):
            self.prerequisites[course_id].remove(prerequisite_id)
            return True
        return False
