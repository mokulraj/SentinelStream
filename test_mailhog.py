from app.worker.celery_app import send_alert_email

# Run immediately in the same process
send_alert_email.apply(
    args=("user@example.com", 12345, 0.95),
    kwargs={
        "amount": 75000,
        "merchant": "Bank of India",
        "transaction_uuid": "test-uuid-001"
    }
)