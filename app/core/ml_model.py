# app/core/ml_model.py

def score_transaction(tx: dict) -> float:
    """
    Mock ML model to generate risk score (0.0 - 1.0)
    - High amount → high risk
    """
    amount = tx.get("amount", 0)
    if amount > 5000:
        return 0.9
    elif amount > 1000:
        return 0.6
    return 0.1
