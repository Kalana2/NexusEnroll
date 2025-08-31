from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from models.course import Course


class CourseEvent(BaseModel):
    event_type: str
    course_id: str
    timestamp: datetime = datetime.now()
    service_name: str = "course-service"

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class CourseCreatedEvent(CourseEvent):
    event_type: str = "course_created"
    course_data: Course


class CourseUpdatedEvent(CourseEvent):
    event_type: str = "course_updated"
    updated_fields: Dict[str, Any]
    course_data: Course


class CourseDeletedEvent(CourseEvent):
    event_type: str = "course_deleted"


class CourseFullEvent(CourseEvent):
    event_type: str = "course_full"
    current_enrollment: int
    total_capacity: int


class CourseCapacityChangedEvent(CourseEvent):
    event_type: str = "course_capacity_changed"
    old_capacity: int
    new_capacity: int


class CourseEnrollmentEvent(CourseEvent):
    event_type: str = "course_enrollment_changed"
    action: str  # "enrolled" or "dropped"
    student_id: str
    current_enrollment: int
    total_capacity: int


class PrerequisiteAddedEvent(CourseEvent):
    event_type: str = "prerequisite_added"
    prerequisite_course_id: str


class PrerequisiteRemovedEvent(CourseEvent):
    event_type: str = "prerequisite_removed"
    prerequisite_course_id: str


# Event types for reference
COURSE_EVENT_TYPES = {
    "course_created": CourseCreatedEvent,
    "course_updated": CourseUpdatedEvent,
    "course_deleted": CourseDeletedEvent,
    "course_full": CourseFullEvent,
    "course_capacity_changed": CourseCapacityChangedEvent,
    "course_enrollment_changed": CourseEnrollmentEvent,
    "prerequisite_added": PrerequisiteAddedEvent,
    "prerequisite_removed": PrerequisiteRemovedEvent,
}
