# train_model.py
from sklearn.ensemble import IsolationForest
import joblib
import random
from pathlib import Path

# Path to save the model
MODEL_PATH = Path.cwd() / "app/ml/trained_model.pkl"

# Ensure the folder exists
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

# Generate sample data (replace with your real features later)
data = [[random.randint(10, 1000)] for _ in range(200)]

# Train Isolation Forest
model = IsolationForest()
model.fit(data)

# Save the trained model
joblib.dump(model, MODEL_PATH)
print(f"Model saved successfully at: {MODEL_PATH}")
