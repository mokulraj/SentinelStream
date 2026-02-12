# app/worker/celery_app.py

from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Celery config
# Use in-memory broker for dev, Redis/RabbitMQ for prod
celery_app = Celery(
    "sentinelstream",
    broker=os.environ.get("CELERY_BROKER", "memory://"),
    backend=os.environ.get("CELERY_BACKEND", "rpc://"),
)

@celery_app.task
def send_alert_email(
    to_email: str,
    txn_id: int,
    risk_score: float,
    amount: float = None,
    merchant: str = None,
    transaction_uuid: str = None,
):
    """
    Sends an alert email for high-risk transactions.
    Uses MailHog if EMAIL_DEV=True.
    """
    sender_email = os.environ.get("EMAIL_USER", "test@example.com")
    sender_password = os.environ.get("EMAIL_PASS", "")

    use_mailhog = os.environ.get("EMAIL_DEV", "True").lower() in ["true", "1", "yes"]

    subject = f"Alert: Suspicious Transaction #{txn_id}"
    body = f"""
Dear User,

A transaction with ID {txn_id} has been flagged as suspicious.

Risk Score: {risk_score:.2f}
Amount: {amount}
Merchant: {merchant}
Transaction UUID: {transaction_uuid}

Please review this transaction immediately.

Regards,
SentinelStream Team
"""

    # Build the message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        if use_mailhog:
            print(f"[DEV] Sending email to {to_email} via MailHog...")
            with smtplib.SMTP("localhost", 1025) as server:
                server.sendmail(sender_email, to_email, message.as_string())
            print(f"[DEV] Email captured by MailHog for {to_email}")
        else:
            print(f"[PROD] Sending email to {to_email} via Gmail...")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            print(f"[PROD] Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")