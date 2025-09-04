class EmailChannel:
    @staticmethod
    def send(target: str, message: str) -> bool:
        print(f"[Email] Sending to {target}: {message}")
        # integrate with SMTP or SendGrid here
        return True
