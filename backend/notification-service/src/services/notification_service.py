from src.channels.email_channel import EmailChannel
from src.channels.sms_channel import SMSChannel
from src.channels.webpush_channel import WebPushChannel
from src.services.subscription_service import SubscriptionService
from typing import Optional

from supabase import Client, create_client

SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


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

            class SupabaseRepository:
                def __init__(self, client):
                    self.client = client

                def get_subscribers(self, event_type: str):
                    resp = (
                        self.client.table("subscriptions")
                        .select("*")
                        .eq("event_type", event_type)
                        .execute()
                    )
                    if resp.error:
                        raise RuntimeError(f"Supabase error: {resp.error}")
                    return resp.data or []

                def create_subscription(
                    self, user_id: str, event_type: str, channel: str, target: str
                ):
                    payload = {
                        "user_id": user_id,
                        "event_type": event_type,
                        "channel": channel,
                        "target": target,
                    }
                    resp = self.client.table("subscriptions").insert(payload).execute()
                    if resp.error:
                        raise RuntimeError(f"Supabase error: {resp.error}")
                    return resp.data

                def delete_subscription(self, subscription_id):
                    resp = (
                        self.client.table("subscriptions")
                        .delete()
                        .eq("id", subscription_id)
                        .execute()
                    )
                    if resp.error:
                        raise RuntimeError(f"Supabase error: {resp.error}")
                    return resp.data

                def log_notification(
                    self,
                    user_id: str,
                    event_type: str,
                    channel: str,
                    target: str,
                    message: str,
                    status: str,
                ):
                    payload = {
                        "user_id": user_id,
                        "event_type": event_type,
                        "channel": channel,
                        "target": target,
                        "message": message,
                        "status": status,
                    }
                    resp = self.client.table("notifications").insert(payload).execute()
                    if resp.error:
                        raise RuntimeError(f"Supabase error: {resp.error}")
                    return resp.data

                def get_notifications(
                    self, user_id: Optional[str] = None, limit: int = 100
                ):
                    q = (
                        self.client.table("notifications")
                        .select("*")
                        .order("created_at", {"ascending": False})
                        .limit(limit)
                    )
                    if user_id:
                        q = q.eq("user_id", user_id)
                    resp = q.execute()
                    if resp.error:
                        raise RuntimeError(f"Supabase error: {resp.error}")
                    return resp.data or []
                    return resp.data or []

            # convenience single-instance repository using the module-level client
            repository = SupabaseRepository(supabase)
