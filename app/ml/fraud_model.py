# app/ml/fraud_model.py
import random

def get_risk_score(amount: float, txn_count_today: int) -> float:
    """
    Dummy risk score function for testing.
    Returns a float between 0.0 and 1.0
    """
    base_score = amount / 10000  # simple proportional score
    noise = random.random() * 0.3
    return min(1.0, base_score + noise)