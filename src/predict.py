import pandas as pd
import joblib


MODEL_PATH = "models/balanced_logistic_regression.pkl"

model = joblib.load(MODEL_PATH)


def predict_credit_risk(customer_data):
    customer_df = pd.DataFrame([customer_data])

    prediction = model.predict(customer_df)[0]
    prediction_proba = model.predict_proba(customer_df)[0]

    result = {
        "prediction": int(prediction),
        "prediction_label": "Kötü kredi riski" if prediction == 0 else "İyi kredi riski",
        "bad_credit_probability": float(round(prediction_proba[0], 3)),
        "good_credit_probability": float(round(prediction_proba[1], 3))
    }

    return result