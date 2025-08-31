from typing import List, Dict, Optional
from ..models.course import Course
from ..models.course_trend import CourseTrend
from ..repositories.course_repository import CourseRepository
from ..repositories.analytics_repository import AnalyticsRepository
from ..events.event_publisher import EventPublisher


class CourseService:
    def __init__(self):
        self.course_repo = CourseRepository()
        self.analytics_repo = AnalyticsRepository()
        self.event_publisher = EventPublisher()

    def browse_courses(self, filters: Dict) -> List[Course]:
        """Browse courses with optional filters"""
        return self.course_repo.find_courses(filters)

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
            self.event_publisher.publish_course_updated(updated_course)
        return updated_course
