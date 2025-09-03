import smtplib
from email.mime.text import MIMEText

class EmailChannel:
    def __init__(self, smtp_server="localhost", smtp_port=1025):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send(self, target, message):
        """Send email to target (user email)."""
        try:
            msg = MIMEText(message)
            msg["Subject"] = "NexusEnroll Notification"
            msg["From"] = "noreply@nexusuniversity.edu"
            msg["To"] = target

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.sendmail(msg["From"], [msg["To"]], msg.as_string())
            print(f"[EmailChannel] Sent email to {target}: {message}")
            return True
        except Exception as e:
            print(f"[EmailChannel] Failed: {e}")
            return False
