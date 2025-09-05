class SMSChannel:
    @staticmethod
    def send(target: str, message: str) -> bool:
        print(f"[SMS] Sending to {target}: {message}")
        # integrate with Twilio or Nexmo here
        return True
