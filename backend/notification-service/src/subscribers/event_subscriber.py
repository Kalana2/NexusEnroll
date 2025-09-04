from fastapi import APIRouter
from src.services.notification_service import NotificationService
from src.services.subscription_service import SubscriptionService

router = APIRouter()

subscription_service = SubscriptionService()
notification_service = NotificationService(subscription_service)

@router.post("/events/publish")
def publish_event(event_type: str, payload: dict):
    notification_service.publish_event(event_type, payload)
    return {"status": "event published"}
