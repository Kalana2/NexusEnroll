from typing import List
from datetime import datetime, timedelta
from ..models.course_trend import CourseTrend
from ..repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:
    def __init__(self):
        self.analytics_repo = AnalyticsRepository()

    def calculate_course_trends(self) -> List[CourseTrend]:
        """Calculate trending data for all courses"""
        # This would typically involve complex analytics
        # For simplicity, we'll just get the data from the repository
        return self.analytics_repo.get_trending_courses()

    def update_course_analytics(self, course_id: str, enrollment_change: int = 0):
        """Update analytics for a specific course"""
        self.analytics_repo.record_enrollment_change(course_id, enrollment_change)

    def get_popular_courses(self, limit: int = 10) -> List[CourseTrend]:
        """Get the most popular courses"""
        trends = self.analytics_repo.get_trending_courses()
        # Sort by popularity score and return top N
        return sorted(trends, key=lambda x: x.popularity_score, reverse=True)[:limit]
