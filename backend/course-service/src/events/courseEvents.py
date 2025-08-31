from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.course import Course


class CourseEvent(BaseModel):
    event_type: str
    course_id: str
    timestamp: datetime = datetime.now()


class CourseCreatedEvent(CourseEvent):
    event_type: str = "course_created"
    course_data: Course


class CourseUpdatedEvent(CourseEvent):
    event_type: str = "course_updated"
    updated_fields: dict
    course_data: Course


class CourseFullEvent(CourseEvent):
    event_type: str = "course_full"
    current_enrollment: int
    total_capacity: int


class CourseCapacityChangedEvent(CourseEvent):
    event_type: str = "course_capacity_changed"
    old_capacity: int
    new_capacity: int
