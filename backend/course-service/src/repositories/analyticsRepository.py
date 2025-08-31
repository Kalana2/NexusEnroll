from typing import List
from datetime import datetime
from models.courseTrend import CourseTrend


class AnalyticsRepository:
    def __init__(self):
        # In a real implementation, this would connect to a analytics database
        # For this example, we'll use sample data
        pass

    def get_trending_courses(self) -> List[CourseTrend]:
        """Get trending course data"""
        # Sample data - in a real implementation, this would be calculated
        # based on enrollment patterns, waitlist data, etc.
        return [
            CourseTrend(
                course_id="CS101",
                course_name="Introduction to Computer Science",
                popularity_score=8.5,
                enrollment_rate=0.85,
                waitlist_count=15,
                trend_direction="up",
                last_updated=datetime.now(),
            ),
            CourseTrend(
                course_id="CS201",
                course_name="Data Structures and Algorithms",
                popularity_score=9.2,
                enrollment_rate=0.94,
                waitlist_count=22,
                trend_direction="up",
                last_updated=datetime.now(),
            ),
            CourseTrend(
                course_id="MATH101",
                course_name="Calculus I",
                popularity_score=7.8,
                enrollment_rate=0.92,
                waitlist_count=8,
                trend_direction="stable",
                last_updated=datetime.now(),
            ),
            CourseTrend(
                course_id="CS301",
                course_name="Database Systems",
                popularity_score=8.1,
                enrollment_rate=0.75,
                waitlist_count=12,
                trend_direction="up",
                last_updated=datetime.now(),
            ),
            CourseTrend(
                course_id="PHYS101",
                course_name="Physics I",
                popularity_score=6.9,
                enrollment_rate=0.81,
                waitlist_count=5,
                trend_direction="down",
                last_updated=datetime.now(),
            ),
        ]

    def record_enrollment_change(self, course_id: str, change: int):
        """Record an enrollment change for analytics"""
        # In a real implementation, this would store data for later analysis
        pass
