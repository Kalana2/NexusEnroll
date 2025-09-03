import uuid

class SubscriptionManager:
    def __init__(self):
        # In-memory storage {userId: [ {id, eventType, channel, target} ]}
        self.subscriptions = {}

    def subscribe(self, user_id, event_type, channel, target):
        sub_id = str(uuid.uuid4())
        record = {"id": sub_id, "eventType": event_type, "channel": channel, "target": target}

        if user_id not in self.subscriptions:
            self.subscriptions[user_id] = []
        self.subscriptions[user_id].append(record)

        print(f"[SubscriptionManager] User {user_id} subscribed to {event_type} via {channel}")
        return sub_id

    def list_subscriptions(self, user_id):
        return self.subscriptions.get(user_id, [])

    def get_subscribers_for_event(self, event_type):
        """Return all (userId, channel, target) subscribed to this event."""
        results = []
        for user_id, subs in self.subscriptions.items():
            for s in subs:
                if s["eventType"] == event_type:
                    results.append((user_id, s["channel"], s["target"]))
        return results
