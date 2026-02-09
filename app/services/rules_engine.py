def apply_rules(transaction: dict) -> dict:
    """
    Simple rule-based fraud detection (starter logic)
    """

    amount = transaction.get("amount", 0)
    country = transaction.get("country", "").lower()

    # Default decision
    decision = "approve"
    reason = "Transaction approved"

    if amount > 100000:
        decision = "flag"
        reason = "High transaction amount"

    if country in ["north korea", "iran"]:
        decision = "decline"
        reason = "Restricted country"

    return {
        "decision": decision,
        "reason": reason
    }
