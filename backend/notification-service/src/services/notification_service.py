from src.channels.email_channel import EmailChannel
from src.channels.sms_channel import SMSChannel
from src.channels.webpush_channel import WebPushChannel
from src.services.subscription_manager import SubscriptionManager

class NotificationService:
    def __init__(self):
        self.subscription_manager = SubscriptionManager()
        self.email_channel = EmailChannel()
        self.sms_channel = SMSChannel()
        self.web_channel = WebPushChannel()

    def send_notification(self, user_id, message, channel, target):
        """Send a direct notification to a user."""
        if channel == "Email":
            return self.email_channel.send(target, message)
        elif channel == "SMS":
            return self.sms_channel.send(target, message)
        elif channel == "Web":
            return self.web_channel.send(user_id, message)
        else:
            print(f"[NotificationService] Unknown channel {channel}")
            return False

    def publish_event(self, event_type, payload):
        """Publish event → notify subscribers."""
        subscribers = self.subscription_manager.get_subscribers_for_event(event_type)
        print(f"[NotificationService] Publishing event {event_type} to {len(subscribers)} subs")
        for user_id, channel, target in subscribers:
            message = f"Event {event_type} occurred. Details: {payload}"
            self.send_notification(user_id, message, channel, target)
