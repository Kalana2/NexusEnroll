from fastapi import FastAPI
import importlib
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


# Dynamically import the subscriber module and attach a router if it exposes one.
# This avoids a hard attribute access that may not exist (e.g. router vs event_router).
try:
    mod = importlib.import_module("src.subscribers.event_subscriber")
except Exception:
    mod = None

if mod is not None:
    for attr_name in ("router", "event_router", "api_router"):
        router = getattr(mod, attr_name, None)
        if router is not None:
            app.include_router(router)
            break
    else:
        # No router found on the module; nothing to include.
        pass
