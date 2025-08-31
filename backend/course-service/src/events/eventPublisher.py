import redis
import json
from ..config import settings
from .course_events import (
    CourseEvent,
    CourseUpdatedEvent,
    CourseFullEvent,
    CourseCapacityChangedEvent,
)


class EventPublisher:
    def __init__(self):
        # In a real implementation, this would connect to a message broker
        # For this example, we'll simulate the connection
        try:
            self.redis_client = redis.Redis.from_url(settings.MESSAGE_BROKER_URL)
        except:
            self.redis_client = None
            print("Warning: Could not connect to Redis. Events will not be published.")

    def publish_event(self, event: CourseEvent):
        """Publish an event to the message bus"""
        if not self.redis_client:
            return False

        try:
            channel = f"course_events_{event.event_type}"
            self.redis_client.publish(channel, event.json())
            return True
        except Exception as e:
            print(f"Error publishing event: {e}")
            return False

    def publish_course_updated(self, course, updated_fields=None):
        """Publish a course updated event"""
        event = CourseUpdatedEvent(
            course_id=course.id, updated_fields=updated_fields or {}, course_data=course
        )
        return self.publish_event(event)

    def publish_course_full(self, course_id, current_enrollment, total_capacity):
        """Publish a course full event"""
        event = CourseFullEvent(
            course_id=course_id,
            current_enrollment=current_enrollment,
            total_capacity=total_capacity,
        )
        return self.publish_event(event)

    def publish_capacity_changed(self, course_id, old_capacity, new_capacity):
        """Publish a capacity changed event"""
        event = CourseCapacityChangedEvent(
            course_id=course_id, old_capacity=old_capacity, new_capacity=new_capacity
        )
        return self.publish_event(event)
