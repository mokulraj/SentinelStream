from app.ml.model import predict

def check_fraud(amount: float):
    ml_result = predict(amount)

    rules_flag = False
    if amount > 10000:
        rules_flag = True

    is_fraud = ml_result == -1 or rules_flag

    return is_fraud
