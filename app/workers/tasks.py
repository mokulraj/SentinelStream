# app/workers/tasks.py
def send_fraud_alert(transaction_id: str, message: str):
    # For now, just print to console
    print(f"Fraud alert for transaction {transaction_id}: {message}")
