import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.predict import predict_credit_risk


st.set_page_config(
    page_title="AI Kredi Skorlama Sistemi",
    page_icon="🏦",
    layout="wide",
)


STATUS = {
    "Borçlu / negatif bakiye (< 0 DM)": 1,
    "Düşük bakiye (0 - 200 DM)": 2,
    "Orta bakiye (> 200 DM)": 3,
    "Hesap yok / özel kategori": 4,
}

SAVINGS = {
    "Çok düşük (< 100 DM)": 1,
    "Düşük (100 - 500 DM)": 2,
    "Orta (500 - 1000 DM)": 3,
    "Yüksek (> 1000 DM)": 4,
    "Bilinmiyor / özel kategori": 5,
}

EMPLOYMENT = {
    "İşsiz": 1,
    "1 yıldan az": 2,
    "1 - 4 yıl": 3,
    "4 - 7 yıl": 4,
    "7 yıldan fazla": 5,
}

CREDIT_HISTORY = {
    "Sınırlı kredi geçmişi": 0,
    "Geçmişte ciddi sorun": 1,
    "Mevcut krediler düzenli ödenmiş": 2,
    "Geçmişte gecikme olmuş": 3,
    "Tüm krediler düzenli ödenmiş": 4,
}

PURPOSE = {
    "Araç": 0,
    "Mobilya / ekipman": 1,
    "Radyo / TV": 2,
    "Ev aletleri": 3,
    "Tamirat": 4,
    "Eğitim": 5,
    "Tatil / diğer": 6,
    "Yeniden eğitim": 8,
    "İş / ticari amaç": 9,
    "Diğer": 10,
}

INSTALLMENT = {
    "Çok yüksek yük (gelirin %35+ kısmı)": 1,
    "Yüksek yük (%25 - %35)": 2,
    "Orta yük (%20 - %25)": 3,
    "Düşük yük (%20 altı)": 4,
}

HOUSING = {
    "Kirada": 1,
    "Kendi evi": 2,
    "Ücretsiz / aile yanında": 3,
}

PROPERTY = {
    "Gayrimenkul": 1,
    "Birikim / hayat sigortası": 2,
    "Araç veya diğer mülk": 3,
    "Mülk yok / bilinmiyor": 4,
}

PERSONAL_STATUS = {
    "Erkek - ayrılmış / boşanmış": 1,
    "Kadın - evli / ayrılmış": 2,
    "Erkek - bekar": 3,
    "Erkek - evli / dul": 4,
}

OTHER_DEBTORS = {
    "Yok": 1,
    "Ortak başvuru sahibi": 2,
    "Kefil var": 3,
}

RESIDENCE = {
    "1 yıldan az": 1,
    "1 - 4 yıl": 2,
    "4 - 7 yıl": 3,
    "7 yıldan fazla": 4,
}

OTHER_INSTALLMENT = {
    "Banka": 1,
    "Mağaza": 2,
    "Yok": 3,
}

NUMBER_CREDITS = {
    "1 kredi": 1,
    "2 kredi": 2,
    "3 kredi": 3,
    "4 veya daha fazla": 4,
}

JOB = {
    "İşsiz / vasıfsız": 1,
    "Vasıfsız çalışan": 2,
    "Nitelikli çalışan": 3,
    "Yönetici / uzman / serbest meslek": 4,
}

PEOPLE_LIABLE = {
    "3 veya daha fazla kişi": 1,
    "0 - 2 kişi": 2,
}

TELEPHONE = {
    "Kayıtlı telefon yok": 1,
    "Kayıtlı telefon var": 2,
}

FOREIGN_WORKER = {
    "Evet": 1,
    "Hayır": 2,
}


def build_customer_data(
    status_label,
    duration,
    credit_history_label,
    purpose_label,
    amount,
    savings_label,
    employment_label,
    installment_label,
    property_label,
    age,
    housing_label,
    personal_label,
    debtor_label,
    residence_label,
    other_installment_label,
    number_credits_label,
    job_label,
    people_label,
    telephone_label,
    foreign_worker_label,
):
    return {
        "status": STATUS[status_label],
        "duration": int(duration),
        "credit_history": CREDIT_HISTORY[credit_history_label],
        "purpose": PURPOSE[purpose_label],
        "amount": int(amount),
        "savings": SAVINGS[savings_label],
        "employment_duration": EMPLOYMENT[employment_label],
        "installment_rate": INSTALLMENT[installment_label],
        "personal_status_sex": PERSONAL_STATUS[personal_label],
        "other_debtors": OTHER_DEBTORS[debtor_label],
        "present_residence": RESIDENCE[residence_label],
        "property": PROPERTY[property_label],
        "age": int(age),
        "other_installment_plans": OTHER_INSTALLMENT[other_installment_label],
        "housing": HOUSING[housing_label],
        "number_credits": NUMBER_CREDITS[number_credits_label],
        "job": JOB[job_label],
        "people_liable": PEOPLE_LIABLE[people_label],
        "telephone": TELEPHONE[telephone_label],
        "foreign_worker": FOREIGN_WORKER[foreign_worker_label],
    }


def decision_text(decision):
    if decision == "APPROVE":
        return "ONAY"
    if decision == "REVIEW":
        return "İNCELEME"
    return "RET"


def score_gauge(score):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " / 850"},
            gauge={
                "axis": {"range": [300, 850]},
                "bar": {"color": "#2563EB"},
                "steps": [
                    {"range": [300, 550], "color": "#FCA5A5"},
                    {"range": [550, 700], "color": "#FDE68A"},
                    {"range": [700, 850], "color": "#86EFAC"},
                ],
            },
        )
    )
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
    return fig


def probability_chart(bad_prob, good_prob):
    fig = go.Figure(
        go.Pie(
            labels=["Risk olasılığı", "Güven olasılığı"],
            values=[bad_prob, good_prob],
            hole=0.55,
        )
    )
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
    return fig


def factor_chart(amount, duration, savings_value, status_value):
    payment_index = amount / duration

    data = pd.DataFrame(
        {
            "Gösterge": [
                "Kredi tutarı",
                "Vade süresi",
                "Ödeme yükü",
                "Birikim seviyesi",
                "Hesap durumu",
            ],
            "Değer": [
                min(amount / 20000 * 100, 100),
                min(duration / 72 * 100, 100),
                min(payment_index / 500 * 100, 100),
                savings_value / 5 * 100,
                status_value / 4 * 100,
            ],
        }
    )

    fig = go.Figure(
        go.Bar(
            x=data["Değer"],
            y=data["Gösterge"],
            orientation="h",
            text=[f"%{v:.0f}" for v in data["Değer"]],
            textposition="auto",
        )
    )

    fig.update_layout(
        height=320,
        xaxis_title="Göreli seviye",
        yaxis_title="",
        margin=dict(l=20, r=20, t=20, b=20),
    )

    return fig


with st.sidebar:
    st.title("🏦 Menü")

    page = st.radio(
        "Sayfa seç",
        [
            "Ana Sayfa",
            "Kredi Başvurusu",
            "Model Sonuçları",
            "Proje Hakkında",
        ],
    )

    st.divider()
    st.write("**Sistem çıktıları:**")
    st.write("• Kredi skoru")
    st.write("• Risk seviyesi")
    st.write("• Karar önerisi")


if page == "Ana Sayfa":
    st.title("🏦 AI Kredi Skorlama Sistemi")

    st.write(
        "Bu uygulama, müşteri kredi başvuru bilgilerini analiz ederek kredi skoru, "
        "risk seviyesi ve APPROVE / REVIEW / DECLINE kararı üretir."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("### 📊 Kredi Skoru\nModel sonucu 300-850 arasında anlaşılır bir skora çevrilir.")

    with c2:
        st.success("### 🛡️ Risk Analizi\nKötü kredi olasılığı ve güven olasılığı hesaplanır.")

    with c3:
        st.warning("### ⚖️ Karar Önerisi\nSistem başvuru için onay, inceleme veya ret önerir.")

    st.subheader("Nasıl Kullanılır?")
    st.write("1. Sol menüden **Kredi Başvurusu** sayfasına geçiniz.")
    st.write("2. Finansal profil, başvuru parametreleri ve ek bilgileri giriniz.")
    st.write("3. **Kredi Riskini Analiz Et** butonuna basınız.")
    st.write("4. Sistem sonucu skor, karar, risk ve grafiklerle gösterir.")


elif page == "Kredi Başvurusu":
    st.title("📝 Kredi Başvurusu")

    st.info(
        "Bu form eğitim amaçlıdır. Kredi miktarı gerçek para birimi değil, "
        "South German Credit veri setindeki kredi tutarı ölçeğidir."
    )

    with st.form("credit_form"):
        st.subheader("💳 Finansal Profil")

        f1, f2, f3 = st.columns(3)

        with f1:
            status_label = st.selectbox("Hesap durumu", list(STATUS.keys()))
            savings_label = st.selectbox("Birikim seviyesi", list(SAVINGS.keys()))

        with f2:
            amount = st.number_input(
                "Kredi miktarı (veri seti ölçeği)",
                min_value=250,
                max_value=20000,
                value=3000,
                step=250,
            )
            duration = st.slider("Kredi süresi (ay)", 4, 72, 24)

        with f3:
            installment_label = st.selectbox("Taksit yükü", list(INSTALLMENT.keys()))
            credit_history_label = st.selectbox("Kredi geçmişi", list(CREDIT_HISTORY.keys()))

        st.subheader("📊 Başvuru Parametreleri")

        p1, p2, p3 = st.columns(3)

        with p1:
            purpose_label = st.selectbox("Kredi amacı", list(PURPOSE.keys()))
            housing_label = st.selectbox("Konut durumu", list(HOUSING.keys()))

        with p2:
            applicant_name = st.text_input("Müşteri adı")
            age = st.slider("Yaş", 18, 80, 35)

        with p3:
            employment_label = st.selectbox("Çalışma süresi", list(EMPLOYMENT.keys()))
            property_label = st.selectbox("Mülkiyet durumu", list(PROPERTY.keys()))

        with st.expander("⚙️ Ek Model Bilgileri"):
            e1, e2, e3 = st.columns(3)

            with e1:
                personal_label = st.selectbox("Medeni / kişisel durum", list(PERSONAL_STATUS.keys()))
                debtor_label = st.selectbox("Diğer borçlu / kefil", list(OTHER_DEBTORS.keys()))

            with e2:
                residence_label = st.selectbox("Mevcut adreste oturma süresi", list(RESIDENCE.keys()))
                other_installment_label = st.selectbox("Diğer taksit planı", list(OTHER_INSTALLMENT.keys()))

            with e3:
                number_credits_label = st.selectbox("Mevcut kredi sayısı", list(NUMBER_CREDITS.keys()))
                job_label = st.selectbox("Meslek türü", list(JOB.keys()))
                people_label = st.selectbox("Bakmakla yükümlü kişi sayısı", list(PEOPLE_LIABLE.keys()))
                telephone_label = st.selectbox("Telefon durumu", list(TELEPHONE.keys()))
                foreign_worker_label = st.selectbox("Yabancı çalışan mı?", list(FOREIGN_WORKER.keys()))

        submitted = st.form_submit_button("Kredi Riskini Analiz Et", use_container_width=True)

    if not submitted:
        st.info("Formu doldurduktan sonra **Kredi Riskini Analiz Et** butonuna basınız.")

    if submitted:
        customer_data = build_customer_data(
            status_label=status_label,
            duration=duration,
            credit_history_label=credit_history_label,
            purpose_label=purpose_label,
            amount=amount,
            savings_label=savings_label,
            employment_label=employment_label,
            installment_label=installment_label,
            property_label=property_label,
            age=age,
            housing_label=housing_label,
            personal_label=personal_label,
            debtor_label=debtor_label,
            residence_label=residence_label,
            other_installment_label=other_installment_label,
            number_credits_label=number_credits_label,
            job_label=job_label,
            people_label=people_label,
            telephone_label=telephone_label,
            foreign_worker_label=foreign_worker_label,
        )

        result = predict_credit_risk(customer_data)

        score = result["credit_score"]
        decision = result["decision"]
        risk_band = result["risk_band"]
        bad_prob = result["bad_credit_probability"]
        good_prob = result["good_credit_probability"]
        payment_index = amount / duration

        st.divider()
        st.header("📌 Kredi Risk Analiz Raporu")

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Kredi Skoru", f"{score} / 850")
        r2.metric("Karar", decision_text(decision))
        r3.metric("Risk Seviyesi", risk_band)
        r4.metric("Risk Olasılığı", f"%{bad_prob * 100:.1f}")

        g1, g2 = st.columns(2)

        with g1:
            st.subheader("Kredi Skoru Göstergesi")
            st.plotly_chart(score_gauge(score), use_container_width=True)

        with g2:
            st.subheader("Risk / Güven Dağılımı")
            st.plotly_chart(probability_chart(bad_prob, good_prob), use_container_width=True)

        st.subheader("Karar Destek Göstergeleri")
        st.write(
            "Bu grafik, başvurudaki temel bilgilerin göreli seviyesini gösterir. "
            "Doğrudan model katsayısı değildir; sonucu kullanıcıya daha anlaşılır göstermek için hazırlanmıştır."
        )

        st.plotly_chart(
            factor_chart(
                amount=amount,
                duration=duration,
                savings_value=SAVINGS[savings_label],
                status_value=STATUS[status_label],
            ),
            use_container_width=True,
        )

        st.subheader("Kısa Yorum")

        name_text = applicant_name if applicant_name else "Bu müşteri"

        st.write(
            f"{name_text} için kredi miktarı **{amount:,.0f} veri seti birimi**, "
            f"vade süresi **{duration} ay** ve ödeme yükü endeksi **{payment_index:,.2f}** olarak hesaplanmıştır."
        )

        if decision == "APPROVE":
            st.success("Model bu başvuruyu düşük riskli görmektedir. Sistem onay önermektedir.")
        elif decision == "REVIEW":
            st.warning("Model bu başvuruyu orta riskli görmektedir. Sistem manuel inceleme önermektedir.")
        else:
            st.error("Model bu başvuruyu yüksek riskli görmektedir. Sistem ret önermektedir.")

        with st.expander("📄 Teknik Dokümantasyon ve Karar Mantığı"):
            st.write("**Seçilen problem:** Kredi skorlama ve risk tahmini")
            st.write("**Model:** Balanced Logistic Regression")
            st.write("**Veri seti:** South German Credit")
            st.write("**Skor aralığı:** 300 düşük, 850 yüksek kredi güvenini temsil eder.")
            st.write("**Karar mantığı:** Model kötü kredi olasılığı üretir; bu olasılık kredi skoruna ve karar sınıfına çevrilir.")
            st.write("**Not:** Bu sistem eğitim amaçlıdır; gerçek bankacılık kararı yerine karar destek prototipi olarak değerlendirilmelidir.")

        with st.expander("Modele gönderilen veri"):
            st.json(customer_data)

        with st.expander("Ham model çıktısı"):
            st.json(result)


elif page == "Model Sonuçları":
    st.title("📈 Model Sonuçları")

    results = pd.DataFrame(
        [
            ["Logistic Regression", 0.790, 0.580],
            ["Balanced Logistic Regression", 0.735, 0.750],
            ["Decision Tree", 0.715, 0.570],
            ["Random Forest", 0.785, 0.420],
        ],
        columns=["Model", "Accuracy", "Kötü Kredi Recall"],
    )

    st.dataframe(results, use_container_width=True, hide_index=True)
    st.bar_chart(results.set_index("Model"))

    st.info(
        "Final model olarak Balanced Logistic Regression seçilmiştir. "
        "Çünkü kredi riski probleminde riskli müşteriyi yakalamak, yalnızca accuracy değerinden daha önemlidir."
    )


elif page == "Proje Hakkında":
    st.title("📘 Proje Hakkında")

    st.write("**Proje konusu:** AI Kredi Skorlama Sistemi")
    st.write("**Veri seti:** South German Credit")
    st.write("**Final model:** Balanced Logistic Regression")
    st.write("**Teknolojiler:** Python, Pandas, Scikit-learn, Joblib, Streamlit, Plotly")
    st.write("**Çıktılar:** Kredi skoru, risk seviyesi, risk olasılığı, APPROVE / REVIEW / DECLINE kararı")