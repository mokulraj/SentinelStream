from pathlib import Path
import joblib

# Build absolute path to the model
MODEL_PATH = Path(__file__).parent / "trained_model.pkl"

# Load model
model = joblib.load(MODEL_PATH)

def predict(value: float) -> int:
    """Return 1 for anomaly, -1 for normal"""
    return model.predict([[value]])[0]
