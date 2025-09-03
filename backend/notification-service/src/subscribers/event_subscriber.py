from src.services.notification_service import NotificationService

class EventSubscriber:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    def on_event(self, event_type, payload):
        """Simulate receiving an event from Enrollment/Grades/etc."""
        print(f"[EventSubscriber] Received {event_type} with payload {payload}")
        self.notification_service.publish_event(event_type, payload)
