import json
import logging
from typing import Optional
from .courseEvents import (
    CourseEvent,
    CourseCreatedEvent,
    CourseUpdatedEvent,
    CourseDeletedEvent,
    CourseFullEvent,
    CourseCapacityChangedEvent,
    CourseEnrollmentEvent,
    PrerequisiteAddedEvent,
    PrerequisiteRemovedEvent,
)

logger = logging.getLogger(__name__)


class EventPublisher:
    def __init__(self):
        # In a real implementation, this would connect to Kafka, RabbitMQ, Redis, etc.
        # For this example, we'll simulate event publishing
        self.connected = True  # Simulate connection status

    def publish_event(self, event: CourseEvent) -> bool:
        """Publish a course event to the message bus"""
        try:
            if not self.connected:
                logger.warning("Event publisher not connected. Event not published.")
                return False

            # Simulate publishing to a message broker
            event_data = event.dict()
            logger.info(
                f"Publishing event: {event_data['event_type']} for course {event_data['course_id']}"
            )

            # In a real implementation, this would send to Kafka/RabbitMQ/Redis
            # Example: self.kafka_producer.send('course-events', event_data)

            return True

        except Exception as e:
            logger.error(f"Error publishing event: {e}")
            return False

    def publish_course_created(self, course) -> bool:
        """Publish a course created event"""
        event = CourseCreatedEvent(course_id=course.id, course_data=course)
        return self.publish_event(event)

    def publish_course_updated(self, course, updated_fields: dict) -> bool:
        """Publish a course updated event"""
        event = CourseUpdatedEvent(
            course_id=course.id, updated_fields=updated_fields, course_data=course
        )
        return self.publish_event(event)

    def publish_course_deleted(self, course_id: str) -> bool:
        """Publish a course deleted event"""
        event = CourseDeletedEvent(course_id=course_id)
        return self.publish_event(event)

    def publish_course_full(
        self, course_id: str, current_enrollment: int, total_capacity: int
    ) -> bool:
        """Publish a course full event"""
        event = CourseFullEvent(
            course_id=course_id,
            current_enrollment=current_enrollment,
            total_capacity=total_capacity,
        )
        return self.publish_event(event)

    def publish_capacity_changed(
        self, course_id: str, old_capacity: int, new_capacity: int
    ) -> bool:
        """Publish a capacity changed event"""
        event = CourseCapacityChangedEvent(
            course_id=course_id, old_capacity=old_capacity, new_capacity=new_capacity
        )
        return self.publish_event(event)

    def publish_enrollment_change(
        self,
        course_id: str,
        action: str,
        student_id: str,
        current_enrollment: int,
        total_capacity: int,
    ) -> bool:
        """Publish an enrollment change event"""
        event = CourseEnrollmentEvent(
            course_id=course_id,
            action=action,
            student_id=student_id,
            current_enrollment=current_enrollment,
            total_capacity=total_capacity,
        )
        return self.publish_event(event)

    def publish_prerequisite_added(
        self, course_id: str, prerequisite_course_id: str
    ) -> bool:
        """Publish a prerequisite added event"""
        event = PrerequisiteAddedEvent(
            course_id=course_id, prerequisite_course_id=prerequisite_course_id
        )
        return self.publish_event(event)

    def publish_prerequisite_removed(
        self, course_id: str, prerequisite_course_id: str
    ) -> bool:
        """Publish a prerequisite removed event"""
        event = PrerequisiteRemovedEvent(
            course_id=course_id, prerequisite_course_id=prerequisite_course_id
        )
        return self.publish_event(event)

    def connect(self):
        """Connect to the message broker"""
        try:
            # Simulate connection
            self.connected = True
            logger.info("Connected to event message broker")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to message broker: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Disconnect from the message broker"""
        self.connected = False
        logger.info("Disconnected from event message broker")
