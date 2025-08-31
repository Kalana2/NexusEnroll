from typing import Dict, List
from ..models.course import Course


def apply_course_filters(courses: List[Course], filters: Dict) -> List[Course]:
    """Apply filters to a list of courses"""
    filtered_courses = courses

    # Apply department filter
    if "department" in filters:
        department = filters["department"].lower()
        filtered_courses = [
            course
            for course in filtered_courses
            if department == course.department.lower()
        ]

    # Apply instructor filter
    if "instructor" in filters:
        instructor = filters["instructor"].lower()
        filtered_courses = [
            course
            for course in filtered_courses
            if instructor in course.instructor.lower()
        ]

    return filtered_courses
