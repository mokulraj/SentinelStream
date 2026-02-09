def final_decision(rule_result: str, ml_score: float):
    if rule_result == "HIGH" or ml_score > 0.8:
        return "DECLINED"

    if rule_result == "MEDIUM" or ml_score > 0.5:
        return "FLAGGED"

    return "APPROVED"
