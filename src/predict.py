import pandas as pd
import joblib


MODEL_PATH = "models/balanced_logistic_regression.pkl"

model = joblib.load(MODEL_PATH)


# Kötü kredi olasılığını 300–850 arasında bir kredi skoruna çevirir.
def calculate_credit_score(bad_credit_probability):
    credit_score = 300 + (1 - bad_credit_probability) * 550
    return int(round(credit_score))


# Risk olasılığına göre APPROVE, REVIEW veya DECLINE kararı üretir.
def make_credit_decision(bad_credit_probability):
    if bad_credit_probability < 0.25:
        return "APPROVE"
    elif bad_credit_probability < 0.55:
        return "REVIEW"
    else:
        return "DECLINE"


# Risk olasılığını Low Risk, Medium Risk veya High Risk olarak etiketler.
def get_risk_band(bad_credit_probability):
    if bad_credit_probability < 0.25:
        return "Low Risk"
    elif bad_credit_probability < 0.55:
        return "Medium Risk"
    else:
        return "High Risk"


def predict_credit_risk(customer_data):
    customer_df = pd.DataFrame([customer_data])

    prediction = model.predict(customer_df)[0]
    prediction_proba = model.predict_proba(customer_df)[0]

    bad_credit_probability = float(round(prediction_proba[0], 3))
    good_credit_probability = float(round(prediction_proba[1], 3))

    credit_score = calculate_credit_score(bad_credit_probability)
    decision = make_credit_decision(bad_credit_probability)
    risk_band = get_risk_band(bad_credit_probability)

    result = {
        "prediction": int(prediction),
        "prediction_label": "Kötü kredi riski" if prediction == 0 else "İyi kredi riski",
        "bad_credit_probability": bad_credit_probability,
        "good_credit_probability": good_credit_probability,
        "credit_score": credit_score,
        "decision": decision,
        "risk_band": risk_band
    }

    return result