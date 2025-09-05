from fastapi import FastAPI
from src.subscribers import event_subscriber
from src.services.subscription_service import SubscriptionService
from src.services.notification_service import NotificationService

app = FastAPI(title="Notification Service")

subscription_service = SubscriptionService()
notification_service = NotificationService(subscription_service)


@app.get("/")
def read_root():
    return {"message": "Notification Service is running"}


@app.post("/subscribe")
def subscribe(user_id: str, event_type: str, channel: str, target: str):
    sub_id = subscription_service.subscribe(user_id, event_type, channel, target)
    return {"subscription_id": sub_id}


@app.get("/subscriptions/{user_id}")
def list_subscriptions(user_id: str):
    subs = subscription_service.list_subscriptions(user_id)
    return [
        {"id": s.id, "event": s.event_type, "channel": s.channel, "target": s.target}
        for s in subs
    ]


app.include_router(event_subscriber.router)
