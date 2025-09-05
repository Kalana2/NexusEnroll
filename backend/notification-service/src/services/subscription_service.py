from typing import Dict, List
from uuid import uuid4

class Subscription:
    def __init__(self, user_id: str, event_type: str, channel: str, target: str):
        self.id = str(uuid4())
        self.user_id = user_id
        self.event_type = event_type
        self.channel = channel
        self.target = target

class SubscriptionService:
    def __init__(self):
        # in-memory storage (replace with DB in production)
        self.subscriptions: Dict[str, Subscription] = {}

    def subscribe(self, user_id: str, event_type: str, channel: str, target: str) -> str:
        sub = Subscription(user_id, event_type, channel, target)
        self.subscriptions[sub.id] = sub
        return sub.id

    def list_subscriptions(self, user_id: str) -> List[Subscription]:
        return [s for s in self.subscriptions.values() if s.user_id == user_id]

    def get_subscribers(self, event_type: str) -> List[Subscription]:
        return [s for s in self.subscriptions.values() if s.event_type == event_type]
