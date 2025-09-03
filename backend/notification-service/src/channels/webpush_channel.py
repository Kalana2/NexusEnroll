class WebPushChannel:
    def __init__(self):
        self.web_clients = {}  # mapping userId -> socket/session

    def register_client(self, user_id, client_conn):
        """Register a web client (e.g., websocket)."""
        self.web_clients[user_id] = client_conn

    def send(self, target, message):
        """Send via WebSocket (simulated)."""
        if target in self.web_clients:
            print(f"[WebPushChannel] Sending WebPush to {target}: {message}")
            return True
        else:
            print(f"[WebPushChannel] No active web client for {target}")
            return False
