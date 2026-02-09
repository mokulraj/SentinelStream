# app/services/ml_engine.py
import os
import joblib

MODEL_PATH = "models/isolation_forest.pkl"

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    print("⚠️ ML model not found, using fallback scoring")

def ml_risk_score(features: dict) -> float:
    if model is None:
        return 0.3  # safe fallback score

    score = model.decision_function([list(features.values())])[0]
    return float(score)
