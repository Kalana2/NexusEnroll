from typing import List, Dict, Optional
from models.course import Course
from models.courseTrend import CourseTrend
from repositories.courseRepository import CourseRepository
from repositories.analyticsRepository import AnalyticsRepository
from events.eventPublisher import EventPublisher
from utils.filters import apply_course_filters


class CourseService:
    def __init__(self):
        self.course_repo = CourseRepository()
        self.analytics_repo = AnalyticsRepository()
        self.event_publisher = EventPublisher()

    def browse_courses(self, keywords: Optional[str], filters: Dict) -> List[Course]:
        """Browse courses with optional keywords and filters"""
        all_courses = self.course_repo.find_all_courses()

        # Apply keyword filtering if provided
        if keywords:
            filtered_courses = []
            keyword_lower = keywords.lower()
            for course in all_courses:
                if (
                    keyword_lower in course.name.lower()
                    or keyword_lower in course.description.lower()
                    or keyword_lower in course.department.lower()
                    or keyword_lower in course.instructor.lower()
                ):
                    filtered_courses.append(course)
            all_courses = filtered_courses

        # Apply additional filters
        return apply_course_filters(all_courses, filters)

    def get_course(self, course_id: str) -> Optional[Course]:
        """Get a specific course by ID"""
        return self.course_repo.find_course_by_id(course_id)

    def get_course_capacity(self, course_id: str) -> Optional[Dict]:
        """Get capacity information for a course"""
        course = self.course_repo.find_course_by_id(course_id)
        if not course:
            return None

        return {
            "total": course.total_capacity,
            "remaining": course.total_capacity - course.current_enrollment,
            "current_enrollment": course.current_enrollment,
        }

    def get_courses_trending_data(self) -> List[CourseTrend]:
        """Get trending course data"""
        return self.analytics_repo.get_trending_courses()

    def update_course_info(self, course_id: str, updates: Dict) -> Optional[Course]:
        """Update course information"""
        updated_course = self.course_repo.update_course(course_id, updates)
        if updated_course:
            # Publish course updated event
            self.event_publisher.publish_course_updated(updated_course, updates)
        return updated_course
