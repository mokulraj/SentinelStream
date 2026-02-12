from app.worker.celery_app import send_alert_email

# Example data
to_email = "user@example.com"
txn_id = 123456
risk_score = 0.87

# Send the task to the Celery worker
result = send_alert_email.delay(to_email, txn_id, risk_score)

print(f"Task sent! Task ID: {result.id}")