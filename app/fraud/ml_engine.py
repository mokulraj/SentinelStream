import os
import joblib

MODEL_PATH = "ml/isolation_forest.pkl"

model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print("⚠️ ML model load failed:", e)
        model = None


def ml_risk_score(features: list) -> float:
    if model is None:
        return 0.3  # safe default score
    return float(model.decision_function([features])[0])
