import json
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.predict import predict_credit_risk

SAMPLE_CUSTOMER_PATH = PROJECT_ROOT / "data" / "sample" / "sample_customer.json"


st.set_page_config(
    page_title="Credit Risk Scoring System",
    page_icon="🏦",
    layout="wide"
)


st.title("💳 Credit Risk Scoring System")

st.write(
    "Bu uygulama, South German Credit veri seti kullanılarak geliştirilen "
    "kredi risk tahmin sisteminin kullanıcı arayüzüdür."
)

st.info("Streamlit arayüzü başarıyla çalışıyor.")





st.subheader("Örnek Müşteri Tahmini")

st.write(
    "Aşağıdaki butona basarak `data/sample/sample_customer.json` dosyasındaki "
    "örnek müşteri için kredi risk tahmini yapabilirsiniz."
)

if st.button("Örnek müşteri için tahmin yap"):
    with open(SAMPLE_CUSTOMER_PATH, "r", encoding="utf-8") as file:
        sample_customer = json.load(file)

    result = predict_credit_risk(sample_customer)

    st.success("Tahmin başarıyla tamamlandı.")

    st.write("### Tahmin Sonucu")

    st.write(f"**Prediction Label:** {result['prediction_label']}")
    st.write(f"**Bad Credit Probability:** {result['bad_credit_probability'] * 100:.1f}%")
    st.write(f"**Good Credit Probability:** {result['good_credit_probability'] * 100:.1f}%")
    st.write(f"**Credit Score:** {result['credit_score']} / 850")
    st.write(f"**Decision:** {result['decision']}")
    st.write(f"**Risk Band:** {result['risk_band']}")