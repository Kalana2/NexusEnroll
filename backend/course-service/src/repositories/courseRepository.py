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
                description="Fundamental concepts of computer science and programming",
                department="Computer Science",
                code="CS101",
                instructor="Dr. Jane Smith",
                credits=3,
                total_capacity=100,
                current_enrollment=85,
                prerequisites=[],
                schedule=None,
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
                schedule=None,
            ),
            "CS301": Course(
                id="CS301",
                name="Database Systems",
                description="Design and implementation of database systems",
                department="Computer Science",
                code="CS301",
                instructor="Dr. Alan Turing",
                credits=3,
                total_capacity=60,
                current_enrollment=45,
                prerequisites=["CS201"],
                schedule=None,
            ),
            "MATH101": Course(
                id="MATH101",
                name="Calculus I",
                description="Introduction to differential and integral calculus",
                department="Mathematics",
                code="MATH101",
                instructor="Dr. Robert Johnson",
                credits=4,
                total_capacity=120,
                current_enrollment=110,
                prerequisites=[],
                schedule=None,
            ),
            "MATH201": Course(
                id="MATH201",
                name="Linear Algebra",
                description="Vector spaces, matrices, and linear transformations",
                department="Mathematics",
                code="MATH201",
                instructor="Dr. Emily Chen",
                credits=3,
                total_capacity=90,
                current_enrollment=70,
                prerequisites=["MATH101"],
                schedule=None,
            ),
            "PHYS101": Course(
                id="PHYS101",
                name="Physics I",
                description="Mechanics, heat, and sound",
                department="Physics",
                code="PHYS101",
                instructor="Dr. Michael Brown",
                credits=4,
                total_capacity=80,
                current_enrollment=65,
                prerequisites=[],
                schedule=None,
            ),
        }
        return sample_data

    def find_course_by_id(self, course_id: str) -> Optional[Course]:
        """Find a course by its ID"""
        return self.courses.get(course_id)

    def find_all_courses(self) -> List[Course]:
        """Get all courses"""
        return list(self.courses.values())

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
