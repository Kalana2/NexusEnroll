from fastapi import FastAPI
from src.subscribers import event_subscriber
from src.services.subscription_service import SubscriptionService
from src.services.notification_service import NotificationService

app = FastAPI(title="Notification Service")

subscription_service = SubscriptionService()
notification_service = NotificationService(subscription_service)


@app.post("/events/publish")
def publish_event(event_type: str, payload: dict):
    notification_service.publish_event(event_type, payload)
    return {"status": "event published"}
