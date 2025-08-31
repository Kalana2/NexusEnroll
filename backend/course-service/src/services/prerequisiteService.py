from typing import List, Optional
from models.course import Course
from repositories.prerequisiteRepository import PrerequisiteRepository
from repositories.courseRepository import CourseRepository


class PrerequisiteService:
    def __init__(self):
        self.prerequisite_repo = PrerequisiteRepository()
        self.course_repo = CourseRepository()

    def list_prerequisites(self, course_id: str) -> Optional[List[Course]]:
        """List all prerequisites for a course"""
        # First check if course exists
        course = self.course_repo.find_course_by_id(course_id)
        if not course:
            return None

        # Get prerequisite IDs
        prerequisite_ids = self.prerequisite_repo.find_prerequisites(course_id)

        # Get full course objects for each prerequisite
        prerequisites = []
        for prereq_id in prerequisite_ids:
            prereq_course = self.course_repo.find_course_by_id(prereq_id)
            if prereq_course:
                prerequisites.append(prereq_course)

        return prerequisites

    def add_prerequisite(self, course_id: str, prerequisite_id: str) -> bool:
        """Add a prerequisite to a course"""
        # Check if both courses exist
        course = self.course_repo.find_course_by_id(course_id)
        prerequisite = self.course_repo.find_course_by_id(prerequisite_id)

        if not course or not prerequisite:
            return False

        # Check if prerequisite already exists
        existing = self.prerequisite_repo.find_prerequisite(course_id, prerequisite_id)
        if existing:
            return True  # Already exists, consider it a success

        return self.prerequisite_repo.add_prerequisite(course_id, prerequisite_id)

    def remove_prerequisite(self, course_id: str, prerequisite_id: str) -> bool:
        """Remove a prerequisite from a course"""
        return self.prerequisite_repo.remove_prerequisite(course_id, prerequisite_id)
