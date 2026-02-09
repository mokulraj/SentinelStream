# app/core/rules.py

def evaluate_rules(tx: dict) -> str:
    """
    Simple rule engine:
    - Amount > 5000 AND location != 'UserHome' → RISK
    - Otherwise SAFE
    """
    amount = tx.get("amount", 0)
    location = tx.get("location", "")
    if amount > 5000 and location != "UserHome":
        return "RISK"
    return "SAFE"
