from typing import List, Dict, Optional
from ..models.course import Course
import json
import os


class CourseRepository:
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For this example, we'll use a simple in-memory storage
        self.courses = self._load_sample_data()

    def _load_sample_data(self) -> Dict[str, Course]:
        """Load sample course data"""
        sample_data = {
            "CS101": Course(
                id="CS101",
                name="Introduction to Computer Science",
                description="Fundamental concepts of computer science",
                department="Computer Science",
                code="CS101",
                instructor="Dr. Jane Smith",
                credits=3,
                total_capacity=100,
                current_enrollment=85,
                prerequisites=[],
            ),
            "CS201": Course(
                id="CS201",
                name="Data Structures and Algorithms",
                description="Study of fundamental data structures and algorithms",
                department="Computer Science",
                code="CS201",
                instructor="Dr. John Doe",
                credits=4,
                total_capacity=80,
                current_enrollment=75,
                prerequisites=["CS101"],
            ),
            "MATH101": Course(
                id="MATH101",
                name="Calculus I",
                description="Introduction to differential and integral calculus",
                department="Mathematics",
                code="MATH101",
                instructor="Dr. Alan Turing",
                credits=4,
                total_capacity=120,
                current_enrollment=110,
                prerequisites=[],
            ),
        }
        return sample_data

    def find_course_by_id(self, course_id: str) -> Optional[Course]:
        """Find a course by its ID"""
        return self.courses.get(course_id)

    def find_courses(self, filters: Dict) -> List[Course]:
        """Find courses based on filters"""
        results = list(self.courses.values())

        # Apply filters
        if "keywords" in filters:
            keywords = filters["keywords"].lower()
            results = [
                c
                for c in results
                if keywords in c.name.lower() or keywords in c.description.lower()
            ]

        if "department" in filters:
            department = filters["department"].lower()
            results = [c for c in results if department == c.department.lower()]

        if "instructor" in filters:
            instructor = filters["instructor"].lower()
            results = [c for c in results if instructor in c.instructor.lower()]

        return results

    def update_course(self, course_id: str, updates: Dict) -> Optional[Course]:
        """Update a course with new information"""
        course = self.courses.get(course_id)
        if not course:
            return None

        # Apply updates
        for key, value in updates.items():
            if hasattr(course, key):
                setattr(course, key, value)

        return course
