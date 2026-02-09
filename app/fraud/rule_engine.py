def rule_based_fraud(amount: float, txn_location: str, user_location: str):
    flags = 0

    if amount > 5000:
        flags += 1

    if txn_location.lower() != user_location.lower():
        flags += 1

    if flags == 2:
        return "HIGH"
    elif flags == 1:
        return "MEDIUM"
    return "LOW"
