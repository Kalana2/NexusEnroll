from src.channels.email_channel.py import EmailChannel
from src.channels.sms_channel import SMSChannel
from src.channels.webpush_channel import WebPushChannel
from src.services.subscription_service import SubscriptionService

class NotificationService:
    def __init__(self, subscription_service: SubscriptionService):
        self.subscription_service = subscription_service

    def send_notification(self, user_id: str, message: str, channel: str, target: str):
        if channel == "Email":
            return EmailChannel.send(target, message)
        elif channel == "SMS":
            return SMSChannel.send(target, message)
        elif channel == "Web":
            return WebPushChannel.send(target, message)
        else:
            raise ValueError("Invalid channel")

    def publish_event(self, event_type: str, payload: dict):
        subscribers = self.subscription_service.get_subscribers(event_type)
        for sub in subscribers:
            self.send_notification(sub.user_id, str(payload), sub.channel, sub.target)
