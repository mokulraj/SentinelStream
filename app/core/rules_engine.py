from typing import List
from app.db.models.fraud_rule import FraudRule

def evaluate_transaction(transaction: dict, rules: List[FraudRule]) -> list:
    """
    Returns a list of triggered rules for a transaction.
    transaction = {
        "amount": 1000,
        "location": "chennai",
        "user_home_location": "delhi",
        "timestamp": "2026-02-09T12:00:00"
    }
    """
    triggered = []

    for rule in rules:
        if not rule.enabled:
            continue

        if rule.rule_type == "AMOUNT_LIMIT" and transaction["amount"] > rule.threshold:
            triggered.append(rule.name)

        if rule.rule_type == "LOCATION_MISMATCH" and transaction["location"] != transaction.get("user_home_location"):
            triggered.append(rule.name)

        if rule.rule_type == "MULTI_TXN_SHORT_TIME":
            # Implement later: check previous transactions in DB
            pass

    return triggered
