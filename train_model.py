
import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
DATA_PATH = "dataset/defects.csv"
MODEL_PATH = "models/bug_model.pkl"

df = pd.read_csv(DATA_PATH)

# Features used by the model
features = [
    "lines_of_code",
    "function_count",
    "class_count",
    "if_count",
    "loop_count",
    "exception_count",
    "function_arguments"
]

X = df[features]
y = df["has_defect"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Create and train the model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Evaluate on held-out sample rows
predictions = model.predict(X_test)

print("Model training completed!")
print("Test accuracy:", round(accuracy_score(y_test, predictions), 2))
print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

# Save model and feature names
os.makedirs("models", exist_ok=True)

joblib.dump(
    {
        "model": model,
        "features": features,
        "demo_dataset": True
    },
    MODEL_PATH
)

print(f"\nModel saved to: {MODEL_PATH}")
print("Warning: This model uses illustrative demo data.")
print("Its predictions are not validated defect probabilities.")
