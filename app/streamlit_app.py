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


st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 17px;
        color: #A0A0A0;
        margin-top: 0px;
        margin-bottom: 25px;
    }

    .section-card {
        padding: 18px 22px;
        border-radius: 14px;
        background-color: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 18px;
    }

    .result-card {
        padding: 18px;
        border-radius: 14px;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.10);
        text-align: center;
        min-height: 125px;
    }

    .result-label {
        font-size: 14px;
        color: #B8B8B8;
        margin-bottom: 8px;
    }

    .result-value {
        font-size: 28px;
        font-weight: 800;
    }

    .small-note {
        font-size: 14px;
        color: #A0A0A0;
    }

    .decision-decline {
        color: #FF6B6B;
    }

    .decision-review {
        color: #FFD166;
    }

    .decision-approve {
        color: #06D6A0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.title("🏦 Credit Risk")
    st.caption("AI / ML tabanlı kredi risk karar destek sistemi")

    st.divider()

    st.subheader("Model")
    st.write("Final model adayı:")
    st.success("Balanced Logistic Regression")

    st.write("Veri seti:")
    st.info("South German Credit")

    st.write("Çıktılar:")
    st.markdown(
        """
        - Kötü kredi olasılığı
        - Kredi skoru
        - Karar önerisi
        - Risk bandı
        """
    )

    st.divider()

    st.caption("Demo modu: Örnek müşteri JSON dosyası üzerinden tahmin yapılır.")


st.markdown('<p class="main-title">Credit Risk Scoring System</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Müşteri bilgilerine göre kredi riskini tahmin eden, kredi skoru ve karar önerisi üreten demo arayüz.</p>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="section-card">
        <b>Bu ekranda ne yapılıyor?</b><br>
        Örnek müşteri verisi <code>data/sample/sample_customer.json</code> dosyasından okunur.
        Model bu müşteri için kötü kredi olasılığı üretir. Sistem bu olasılığı kredi skoruna,
        risk bandına ve kredi kararına dönüştürür.
    </div>
    """,
    unsafe_allow_html=True
)


top_col1, top_col2, top_col3 = st.columns(3)

with top_col1:
    st.metric("Model", "Balanced LR")

with top_col2:
    st.metric("Score Range", "300–850")

with top_col3:
    st.metric("Decision Types", "3")


st.divider()

st.subheader("Örnek Müşteri Tahmini")

st.write(
    "Aşağıdaki butona basarak örnek müşteri için kredi risk tahmini yapabilirsiniz."
)

predict_button = st.button(
    "🔍 Örnek müşteri için tahmin yap",
    type="primary",
    use_container_width=True
)


if predict_button:
    with open(SAMPLE_CUSTOMER_PATH, "r", encoding="utf-8") as file:
        sample_customer = json.load(file)

    result = predict_credit_risk(sample_customer)

    decision = result["decision"]

    if decision == "DECLINE":
        decision_class = "decision-decline"
        decision_explanation = "Bu müşteri yüksek riskli göründüğü için kredi başvurusu reddedilmelidir."
    elif decision == "REVIEW":
        decision_class = "decision-review"
        decision_explanation = "Bu müşteri orta risklidir. Manuel inceleme önerilir."
    else:
        decision_class = "decision-approve"
        decision_explanation = "Bu müşteri düşük riskli göründüğü için kredi başvurusu onaylanabilir."

    st.success("Tahmin başarıyla tamamlandı.")

    st.markdown("### Sonuç Özeti")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Credit Score</div>
                <div class="result-value">{result['credit_score']} / 850</div>
                <div class="small-note">Model tabanlı skor</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with result_col2:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Decision</div>
                <div class="result-value {decision_class}">{result['decision']}</div>
                <div class="small-note">Karar önerisi</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with result_col3:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Risk Band</div>
                <div class="result-value">{result['risk_band']}</div>
                <div class="small-note">Risk seviyesi</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Risk Olasılıkları")

    bad_probability = result["bad_credit_probability"]
    good_probability = result["good_credit_probability"]

    prob_col1, prob_col2 = st.columns(2)

    with prob_col1:
        st.write(f"**Bad Credit Probability:** {bad_probability * 100:.1f}%")
        st.progress(bad_probability)

    with prob_col2:
        st.write(f"**Good Credit Probability:** {good_probability * 100:.1f}%")
        st.progress(good_probability)

    st.markdown("### Risk Yorumu")
    st.warning(decision_explanation)

    with st.expander("Örnek müşteri input verisini göster"):
        st.json(sample_customer)

    with st.expander("Ham model çıktısını göster"):
        st.json(result)