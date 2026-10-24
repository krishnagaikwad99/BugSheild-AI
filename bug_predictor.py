
import joblib
import pandas as pd

MODEL_PATH = "models/bug_model.pkl"


def predict_defect_risk(features):
    # Load the trained model
    saved_data = joblib.load(MODEL_PATH)

    model = saved_data["model"]
    feature_names = saved_data["features"]

    # Arrange metrics in the expected feature order
    input_data = pd.DataFrame(
        [[features[name] for name in feature_names]],
        columns=feature_names
    )

    # Predict defect class
    prediction = int(model.predict(input_data)[0])

    # Estimate the model's score for the defect class
    probabilities = model.predict_proba(input_data)[0]
    defect_index = list(model.classes_).index(1)
    score = float(probabilities[defect_index]) * 100

    return {
        "prediction": prediction,
        "risk_score": round(score, 2),
        "demo_model": saved_data.get("demo_dataset", False)
    }
