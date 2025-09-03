from flask import Flask, request, jsonify
from src.services.notification_service import NotificationService
from src.subscribers.event_subscriber import EventSubscriber

app = Flask(__name__)

notification_service = NotificationService()
event_subscriber = EventSubscriber(notification_service)

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    sub_id = notification_service.subscription_manager.subscribe(
        data["userId"], data["eventType"], data["channel"], data["target"]
    )
    return jsonify({"subscriptionId": sub_id})

@app.route("/subscriptions/<user_id>", methods=["GET"])
def list_subscriptions(user_id):
    subs = notification_service.subscription_manager.list_subscriptions(user_id)
    return jsonify(subs)

@app.route("/publish", methods=["POST"])
def publish_event():
    data = request.json
    event_type = data["eventType"]
    payload = data.get("payload", {})
    event_subscriber.on_event(event_type, payload)
    return jsonify({"status": "published", "eventType": event_type})

if __name__ == "__main__":
    app.run(port=5004, debug=True)
