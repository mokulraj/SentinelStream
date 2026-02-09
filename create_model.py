from sklearn.ensemble import IsolationForest
import joblib
import os
import numpy as np

os.makedirs("models", exist_ok=True)

# fake training data
X = np.random.rand(100, 5)

model = IsolationForest(
    n_estimators=100,
    contamination=0.1,
    random_state=42
)

model.fit(X)

joblib.dump(model, "models/isolation_forest.pkl")

print("✅ ML model created successfully")
