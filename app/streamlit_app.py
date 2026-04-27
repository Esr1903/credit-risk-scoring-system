import json
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# PATH SETUP

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.predict import predict_credit_risk


SAMPLE_CUSTOMER_PATH = PROJECT_ROOT / "data" / "sample" / "sample_customer.json"


# PAGE CONFIG

st.set_page_config(
    page_title="AI Credit Risk Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)



# LIGHT CSS ONLY

st.markdown(
    """
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1380px;
}

.stButton > button {
    border-radius: 14px;
    height: 3rem;
    font-weight: 800;
}

div[data-testid="stMetric"] {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 12px 14px;
    background-color: rgba(255,255,255,0.04);
}
</style>
""",
    unsafe_allow_html=True,
)


# OPTION MAPPINGS

STATUS_OPTIONS = {
    "No checking account / weak account status": 1,
    "Low checking account balance": 2,
    "Moderate checking account balance": 3,
    "Strong checking account status": 4,
}

CREDIT_HISTORY_OPTIONS = {
    "No previous credit or limited history": 0,
    "Critical account / past credit issues": 1,
    "Existing credits paid back duly": 2,
    "Delay in paying off in the past": 3,
    "All credits paid back duly": 4,
}

PURPOSE_OPTIONS = {
    "Car or vehicle": 0,
    "Furniture / equipment": 1,
    "Radio / television": 2,
    "Domestic appliances": 3,
    "Repairs": 4,
    "Education": 5,
    "Vacation / others": 6,
    "Retraining": 8,
    "Business": 9,
    "Other purpose": 10,
}

SAVINGS_OPTIONS = {
    "Very low savings": 1,
    "Low savings": 2,
    "Medium savings": 3,
    "High savings": 4,
    "Unknown / no savings information": 5,
}

EMPLOYMENT_OPTIONS = {
    "Unemployed or very short employment": 1,
    "Less than 1 year": 2,
    "1 to 4 years": 3,
    "4 to 7 years": 4,
    "More than 7 years": 5,
}

INSTALLMENT_OPTIONS = {
    "Low installment burden": 1,
    "Moderate installment burden": 2,
    "High installment burden": 3,
    "Very high installment burden": 4,
}

PERSONAL_STATUS_OPTIONS = {
    "Male divorced / separated": 1,
    "Female divorced / separated / married": 2,
    "Male single": 3,
    "Male married / widowed": 4,
}

OTHER_DEBTORS_OPTIONS = {
    "None": 1,
    "Co-applicant": 2,
    "Guarantor": 3,
}

RESIDENCE_OPTIONS = {
    "Less than 1 year": 1,
    "1 to 4 years": 2,
    "4 to 7 years": 3,
    "More than 7 years": 4,
}

PROPERTY_OPTIONS = {
    "Real estate": 1,
    "Building society savings / life insurance": 2,
    "Car or other property": 3,
    "No property / unknown": 4,
}

OTHER_INSTALLMENT_OPTIONS = {
    "Bank": 1,
    "Stores": 2,
    "None": 3,
}

HOUSING_OPTIONS = {
    "Rent": 1,
    "Own": 2,
    "Free": 3,
}

NUMBER_CREDITS_OPTIONS = {
    "1 credit": 1,
    "2 credits": 2,
    "3 credits": 3,
    "4 or more credits": 4,
}

JOB_OPTIONS = {
    "Unemployed / unskilled non-resident": 1,
    "Unskilled resident": 2,
    "Skilled employee / official": 3,
    "Management / self-employed / highly qualified": 4,
}

PEOPLE_LIABLE_OPTIONS = {
    "3 or more people": 1,
    "0 to 2 people": 2,
}

TELEPHONE_OPTIONS = {
    "No registered telephone": 1,
    "Registered telephone": 2,
}

FOREIGN_WORKER_OPTIONS = {
    "Yes": 1,
    "No": 2,
}


# HELPERS

def load_sample_customer() -> dict:
    with open(SAMPLE_CUSTOMER_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def select_index(mapping: dict, value: int) -> int:
    values = list(mapping.values())
    return values.index(value)


def decision_color(decision: str) -> str:
    if decision == "APPROVE":
        return "#22C55E"
    if decision == "REVIEW":
        return "#F59E0B"
    return "#EF4444"


def decision_icon(decision: str) -> str:
    if decision == "APPROVE":
        return "✅"
    if decision == "REVIEW":
        return "🟡"
    return "⛔"


def decision_message(result: dict) -> str:
    decision = result["decision"]

    if decision == "APPROVE":
        return (
            "This applicant shows low repayment risk. "
            "The model recommends approving the application."
        )

    if decision == "REVIEW":
        return (
            "This applicant has medium repayment risk. "
            "The model recommends manual review before the final lending decision."
        )

    return (
        "This applicant shows elevated repayment risk. "
        "The model recommends declining the credit application."
    )


def build_score_gauge(score: int, decision: str) -> go.Figure:
    color = decision_color(decision)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={
                "suffix": " / 850",
                "font": {"size": 44, "color": "#FFFFFF"},
            },
            gauge={
                "shape": "angular",
                "axis": {
                    "range": [300, 850],
                    "tickwidth": 1,
                    "tickcolor": "#CBD5E1",
                    "tickfont": {"size": 12, "color": "#CBD5E1"},
                },
                "bar": {"color": color, "thickness": 0.22},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [300, 550], "color": "rgba(239,68,68,0.28)"},
                    {"range": [550, 700], "color": "rgba(245,158,11,0.28)"},
                    {"range": [700, 850], "color": "rgba(34,197,94,0.28)"},
                ],
                "threshold": {
                    "line": {"color": "#FFFFFF", "width": 4},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        )
    )

    fig.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#FFFFFF"},
    )

    return fig


def build_probability_donut(bad_probability: float) -> go.Figure:
    good_probability = 1 - bad_probability

    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Bad Credit Risk", "Good Credit Probability"],
                values=[bad_probability, good_probability],
                hole=0.68,
                marker=dict(colors=["#EF4444", "#22C55E"]),
                textinfo="none",
            )
        ]
    )

    fig.update_layout(
        height=230,
        margin=dict(l=5, r=5, t=5, b=5),
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#FFFFFF"},
    )

    return fig


def explain_risk_drivers(customer_data: dict, result: dict) -> tuple[list[str], list[str]]:
    risks = []
    strengths = []

    if customer_data["amount"] >= 8000:
        risks.append("High requested credit amount increases repayment pressure.")
    elif customer_data["amount"] <= 2500:
        strengths.append("Lower credit amount may reduce repayment burden.")

    if customer_data["duration"] >= 36:
        risks.append("Long repayment duration increases uncertainty.")
    elif customer_data["duration"] <= 12:
        strengths.append("Shorter duration reduces long-term uncertainty.")

    if customer_data["savings"] in [1, 2]:
        risks.append("Low savings level indicates limited financial buffer.")
    elif customer_data["savings"] in [4, 5]:
        strengths.append("Strong savings profile supports repayment capacity.")

    if customer_data["installment_rate"] == 4:
        risks.append("Very high installment burden can increase default risk.")
    elif customer_data["installment_rate"] in [1, 2]:
        strengths.append("Lower installment burden supports affordability.")

    if customer_data["age"] < 25:
        risks.append("Young applicant profile may require closer income stability review.")
    elif customer_data["age"] >= 35:
        strengths.append("Mature applicant profile may indicate more stable financial behavior.")

    if result["bad_credit_probability"] >= 0.55:
        risks.append("The model estimates high bad-credit probability.")
    elif result["bad_credit_probability"] < 0.25:
        strengths.append("The model estimates low bad-credit probability.")

    return risks, strengths


def initialize_session_state() -> None:
    if "last_applicant_name" not in st.session_state:
        st.session_state.last_applicant_name = ""

    if "last_customer_data" not in st.session_state:
        st.session_state.last_customer_data = None

    if "last_result" not in st.session_state:
        st.session_state.last_result = None


def store_last_result(applicant_name: str, customer_data: dict, result: dict) -> None:
    st.session_state.last_applicant_name = applicant_name
    st.session_state.last_customer_data = customer_data
    st.session_state.last_result = result


# RESULT VIEW

def render_credit_result(applicant_name: str, customer_data: dict, result: dict) -> None:
    score = result["credit_score"]
    decision = result["decision"]
    risk_band = result["risk_band"]
    bad_probability = result["bad_credit_probability"]
    good_probability = result["good_credit_probability"]

    st.success("Credit application analyzed successfully.")

    st.subheader(f"Hello, {applicant_name} 👋")
    st.write(
        "Here is your AI-powered credit risk assessment. "
        "The system estimates repayment risk, generates a model-based credit score, "
        "and returns an approve / review / decline decision."
    )

    score_col, summary_col = st.columns([1.25, 1])

    with score_col:
        with st.container(border=True):
            st.markdown("#### Here is your credit rate 🙂")
            st.plotly_chart(
                build_score_gauge(score, decision),
                use_container_width=True,
            )

    with summary_col:
        with st.container(border=True):
            st.markdown("#### AI Credit Assessment")
            st.write("Final lending recommendation generated by the model.")

            st.metric("Credit Score", f"{score} / 850")
            st.metric("Recommended Decision", f"{decision_icon(decision)} {decision}")
            st.metric("Risk Band", risk_band)

            risk_col_1, risk_col_2 = st.columns(2)

            with risk_col_1:
                st.metric("Bad Risk", f"{bad_probability * 100:.1f}%")

            with risk_col_2:
                st.metric("Good Credit", f"{good_probability * 100:.1f}%")


    st.markdown("### AI Decision Explanation")
    st.info(decision_message(result))

    risks, strengths = explain_risk_drivers(customer_data, result)

    c1, c2 = st.columns(2)

    with c1:
        with st.container(border=True):
            st.markdown("#### Main risk signals")
            if risks:
                for item in risks:
                    st.write(f"• {item}")
            else:
                st.write("• No strong negative risk signal was detected.")

    with c2:
        with st.container(border=True):
            st.markdown("#### Positive signals")
            if strengths:
                for item in strengths:
                    st.write(f"• {item}")
            else:
                st.write("• No strong positive signal was detected.")

    with st.expander("Application data sent to model"):
        st.json(customer_data)

    with st.expander("Raw model output"):
        st.json(result)


# FORM

def build_application_form(default_customer: dict) -> tuple[bool, str, dict]:
    st.markdown("### Applicant Information")
    st.caption(
        "Enter customer application data. The form uses readable business labels "
        "and sends the correct encoded values to the trained ML model."
    )

    with st.form("credit_application_form"):
        applicant_name = st.text_input("Applicant name", value="")

        c1, c2, c3 = st.columns(3)

        with c1:
            status_label = st.selectbox(
                "Checking account status",
                list(STATUS_OPTIONS.keys()),
                index=select_index(STATUS_OPTIONS, default_customer["status"]),
            )
            duration = st.number_input(
                "Credit duration (months)",
                min_value=1,
                max_value=72,
                value=int(default_customer["duration"]),
            )
            credit_history_label = st.selectbox(
                "Credit history",
                list(CREDIT_HISTORY_OPTIONS.keys()),
                index=select_index(CREDIT_HISTORY_OPTIONS, default_customer["credit_history"]),
            )
            purpose_label = st.selectbox(
                "Loan purpose",
                list(PURPOSE_OPTIONS.keys()),
                index=select_index(PURPOSE_OPTIONS, default_customer["purpose"]),
            )
            amount = st.number_input(
                "Credit amount",
                min_value=250,
                max_value=20000,
                value=int(default_customer["amount"]),
            )
            savings_label = st.selectbox(
                "Savings level",
                list(SAVINGS_OPTIONS.keys()),
                index=select_index(SAVINGS_OPTIONS, default_customer["savings"]),
            )
            employment_label = st.selectbox(
                "Employment duration",
                list(EMPLOYMENT_OPTIONS.keys()),
                index=select_index(EMPLOYMENT_OPTIONS, default_customer["employment_duration"]),
            )

        with c2:
            installment_label = st.selectbox(
                "Installment burden",
                list(INSTALLMENT_OPTIONS.keys()),
                index=select_index(INSTALLMENT_OPTIONS, default_customer["installment_rate"]),
            )
            personal_label = st.selectbox(
                "Personal status / sex",
                list(PERSONAL_STATUS_OPTIONS.keys()),
                index=select_index(PERSONAL_STATUS_OPTIONS, default_customer["personal_status_sex"]),
            )
            debtor_label = st.selectbox(
                "Other debtors",
                list(OTHER_DEBTORS_OPTIONS.keys()),
                index=select_index(OTHER_DEBTORS_OPTIONS, default_customer["other_debtors"]),
            )
            residence_label = st.selectbox(
                "Present residence",
                list(RESIDENCE_OPTIONS.keys()),
                index=select_index(RESIDENCE_OPTIONS, default_customer["present_residence"]),
            )
            property_label = st.selectbox(
                "Property",
                list(PROPERTY_OPTIONS.keys()),
                index=select_index(PROPERTY_OPTIONS, default_customer["property"]),
            )
            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=int(default_customer["age"]),
            )
            other_installment_label = st.selectbox(
                "Other installment plans",
                list(OTHER_INSTALLMENT_OPTIONS.keys()),
                index=select_index(OTHER_INSTALLMENT_OPTIONS, default_customer["other_installment_plans"]),
            )

        with c3:
            housing_label = st.selectbox(
                "Housing",
                list(HOUSING_OPTIONS.keys()),
                index=select_index(HOUSING_OPTIONS, default_customer["housing"]),
            )
            number_credits_label = st.selectbox(
                "Number of existing credits",
                list(NUMBER_CREDITS_OPTIONS.keys()),
                index=select_index(NUMBER_CREDITS_OPTIONS, default_customer["number_credits"]),
            )
            job_label = st.selectbox(
                "Job type",
                list(JOB_OPTIONS.keys()),
                index=select_index(JOB_OPTIONS, default_customer["job"]),
            )
            people_label = st.selectbox(
                "People liable",
                list(PEOPLE_LIABLE_OPTIONS.keys()),
                index=select_index(PEOPLE_LIABLE_OPTIONS, default_customer["people_liable"]),
            )
            telephone_label = st.selectbox(
                "Telephone",
                list(TELEPHONE_OPTIONS.keys()),
                index=select_index(TELEPHONE_OPTIONS, default_customer["telephone"]),
            )
            foreign_worker_label = st.selectbox(
                "Foreign worker",
                list(FOREIGN_WORKER_OPTIONS.keys()),
                index=select_index(FOREIGN_WORKER_OPTIONS, default_customer["foreign_worker"]),
            )

        submitted = st.form_submit_button(
            "Analyze Credit Risk",
            type="primary",
            use_container_width=True,
        )

    if not applicant_name.strip():
        applicant_name = "Applicant"

    customer_data = {
        "status": STATUS_OPTIONS[status_label],
        "duration": int(duration),
        "credit_history": CREDIT_HISTORY_OPTIONS[credit_history_label],
        "purpose": PURPOSE_OPTIONS[purpose_label],
        "amount": int(amount),
        "savings": SAVINGS_OPTIONS[savings_label],
        "employment_duration": EMPLOYMENT_OPTIONS[employment_label],
        "installment_rate": INSTALLMENT_OPTIONS[installment_label],
        "personal_status_sex": PERSONAL_STATUS_OPTIONS[personal_label],
        "other_debtors": OTHER_DEBTORS_OPTIONS[debtor_label],
        "present_residence": RESIDENCE_OPTIONS[residence_label],
        "property": PROPERTY_OPTIONS[property_label],
        "age": int(age),
        "other_installment_plans": OTHER_INSTALLMENT_OPTIONS[other_installment_label],
        "housing": HOUSING_OPTIONS[housing_label],
        "number_credits": NUMBER_CREDITS_OPTIONS[number_credits_label],
        "job": JOB_OPTIONS[job_label],
        "people_liable": PEOPLE_LIABLE_OPTIONS[people_label],
        "telephone": TELEPHONE_OPTIONS[telephone_label],
        "foreign_worker": FOREIGN_WORKER_OPTIONS[foreign_worker_label],
    }

    return submitted, applicant_name, customer_data


# PAGES

def render_credit_scoring() -> None:
    st.title("🏦 AI Credit Scoring System")
    st.write(
        "Input customer application data, run the AI/ML risk model, and receive a credit score, "
        "repayment risk estimate, and approve / review / decline decision."
    )

    default_customer = load_sample_customer()
    submitted, applicant_name, customer_data = build_application_form(default_customer)

    if submitted:
        result = predict_credit_risk(customer_data)
        store_last_result(applicant_name, customer_data, result)
        render_credit_result(applicant_name, customer_data, result)
    else:
        st.info(
            "Fill the applicant form and click Analyze Credit Risk to generate a dynamic credit score."
        )


def render_dashboard() -> None:
    st.title("📊 FinTech Credit Risk Dashboard")
    st.write(
        "Proactive AI/ML dashboard for credit scoring, repayment risk evaluation, "
        "decisioning, explainability, and portfolio monitoring."
    )

    if st.session_state.last_result is None:
        st.warning(
            "No active applicant has been scored yet. Go to Credit Scoring and analyze an applicant first."
        )

        sample_customer = load_sample_customer()
        sample_result = predict_credit_risk(sample_customer)

        st.markdown("### Demo Preview")
        render_credit_result("Demo Preview", sample_customer, sample_result)

    else:
        st.markdown("### Latest Applicant Decision")
        render_credit_result(
            st.session_state.last_applicant_name,
            st.session_state.last_customer_data,
            st.session_state.last_result,
        )


def render_model_performance() -> None:
    st.title("📈 Model Performance Analysis")
    st.write(
        "This section explains why the selected model is suitable for credit risk scoring. "
        "In credit risk, catching risky borrowers is more important than accuracy alone."
    )

    data = pd.DataFrame(
        [
            {
                "Model": "Logistic Regression",
                "Accuracy": 0.790,
                "Bad Credit Recall": 0.580,
                "Business Meaning": "Higher total accuracy, weaker at catching risky borrowers",
            },
            {
                "Model": "Balanced Logistic Regression",
                "Accuracy": 0.735,
                "Bad Credit Recall": 0.750,
                "Business Meaning": "Final model; better balance for detecting bad-credit applicants",
            },
            {
                "Model": "Decision Tree",
                "Accuracy": 0.700,
                "Bad Credit Recall": 0.620,
                "Business Meaning": "Interpretable, but less stable",
            },
            {
                "Model": "Random Forest",
                "Accuracy": 0.760,
                "Bad Credit Recall": 0.680,
                "Business Meaning": "Useful benchmark, but final model prioritizes recall balance",
            },
        ]
    )

    st.dataframe(data, use_container_width=True, hide_index=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Selected Model", "Balanced LR")

    with c2:
        st.metric("Bad Credit Recall", "75.0%")

    with c3:
        st.metric("Accuracy", "73.5%")

    st.markdown("### Why bad-credit recall matters")

    st.warning(
        "Approving a risky borrower may be more costly than sending a safe borrower to manual review. "
        "That is why the selected model prioritizes bad-credit recall, not only total accuracy."
    )

    chart_df = data.set_index("Model")[["Accuracy", "Bad Credit Recall"]]
    st.bar_chart(chart_df)

    st.markdown("### Traditional Credit Scoring vs AI/ML Credit Scoring")

    compare = pd.DataFrame(
        [
            {
                "Area": "Data usage",
                "Traditional scoring": "Mostly historical credit and static bureau rules",
                "AI/ML scoring": "Uses application variables and can be extended with banking, payment, mobile or e-commerce behavior",
            },
            {
                "Area": "Decision speed",
                "Traditional scoring": "Often slower and rule-heavy",
                "AI/ML scoring": "Supports real-time scoring and automated decisioning",
            },
            {
                "Area": "Risk insight",
                "Traditional scoring": "Limited segmentation",
                "AI/ML scoring": "Probability-based risk, score bands and decision thresholds",
            },
            {
                "Area": "Governance",
                "Traditional scoring": "Rule documentation",
                "AI/ML scoring": "Requires explainability, monitoring, fairness checks and audit trails",
            },
        ]
    )

    st.dataframe(compare, use_container_width=True, hide_index=True)


def render_system_modules() -> None:
    st.title("🧩 AI Credit Risk System Modules")
    st.write(
        "Product-level modules inspired by modern FinTech credit risk systems. "
        "Implemented features are separated from future enterprise extensions."
    )

    modules = [
        (
            "Data Ingestion & Unification",
            "The prototype collects structured customer application data. In production, it could integrate banking, payment, bureau, mobile, or e-commerce data.",
            "Prototype active",
        ),
        (
            "Real-Time Scoring Engine",
            "The trained ML model instantly returns bad-credit probability, good-credit probability, credit score, decision, and risk band.",
            "Implemented",
        ),
        (
            "Explainable Dashboard",
            "The app displays risk signals, positive signals, probabilities, raw model output, and decision explanation.",
            "Implemented",
        ),
        (
            "Portfolio Monitoring",
            "The monitoring screen simulates borrower risk distribution and high-risk alerts.",
            "Prototype",
        ),
        (
            "Compliance & Reporting",
            "The methodology screen documents target variable, thresholds, score formula, limitations, and governance requirements.",
            "Prototype",
        ),
        (
            "Integration APIs",
            "FastAPI provides backend endpoints such as GET /health and POST /predict.",
            "Implemented",
        ),
    ]

    for i in range(0, len(modules), 3):
        cols = st.columns(3)

        for col, (title, text, status) in zip(cols, modules[i:i + 3]):
            with col:
                with st.container(border=True):
                    st.markdown(f"#### {title}")
                    st.write(text)
                    st.success(status)


def render_portfolio_monitoring() -> None:
    st.title("🔎 Portfolio Monitoring Prototype")
    st.write(
        "Prototype view for monitoring borrower risk distribution, review queue, and high-risk alerts."
    )

    portfolio = pd.DataFrame(
        [
            {"Customer": "C-1001", "Score": 742, "Decision": "APPROVE", "Risk Band": "Low Risk"},
            {"Customer": "C-1002", "Score": 651, "Decision": "REVIEW", "Risk Band": "Medium Risk"},
            {"Customer": "C-1003", "Score": 474, "Decision": "DECLINE", "Risk Band": "High Risk"},
            {"Customer": "C-1004", "Score": 688, "Decision": "REVIEW", "Risk Band": "Medium Risk"},
            {"Customer": "C-1005", "Score": 803, "Decision": "APPROVE", "Risk Band": "Low Risk"},
        ]
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Low Risk Accounts", "2")

    with c2:
        st.metric("Review Queue", "2")

    with c3:
        st.metric("High Risk Alerts", "1")

    st.dataframe(portfolio, use_container_width=True, hide_index=True)

    st.markdown("### Portfolio Decision Distribution")
    st.bar_chart(portfolio["Decision"].value_counts())


def render_methodology() -> None:
    st.title("📘 Methodology & Governance")
    st.write(
        "Transparent explanation of dataset, target variable, score formula, thresholds, and project limitations."
    )

    st.markdown("### Dataset")

    st.write(
        "The project uses the South German Credit dataset. The target variable is `credit_risk`: "
        "`0` means bad credit and `1` means good credit."
    )

    st.markdown("### Model")

    st.write(
        "The final model candidate is Balanced Logistic Regression. It is saved as a pipeline in "
        "`models/balanced_logistic_regression.pkl`."
    )

    st.markdown("### Credit score formula")

    st.code(
        "credit_score = 300 + (1 - bad_credit_probability) * 550",
        language="text",
    )

    st.markdown("### Decision thresholds")

    thresholds = pd.DataFrame(
        [
            {"Bad Credit Probability": "< 0.25", "Decision": "APPROVE", "Risk Band": "Low Risk"},
            {"Bad Credit Probability": "0.25 – 0.55", "Decision": "REVIEW", "Risk Band": "Medium Risk"},
            {"Bad Credit Probability": ">= 0.55", "Decision": "DECLINE", "Risk Band": "High Risk"},
        ]
    )

    st.dataframe(thresholds, use_container_width=True, hide_index=True)

    st.markdown("### Limitations and production requirements")

    st.markdown(
        """
        - This is an educational AI/ML credit scoring prototype.
        - The score is model-based and not an official bank credit score.
        - The current dataset does not include live bank, bureau, mobile, or e-commerce data.
        - Real deployment would require fairness testing, bias monitoring, audit logs, compliance review, and continuous model monitoring.
        - Portfolio monitoring is shown as a prototype module.
        """
    )



# APP ROUTING

initialize_session_state()

with st.sidebar:
    st.title("🏦 AI Credit Risk")
    st.caption("AI/ML-powered FinTech credit decision system")

    page = st.radio(
        "Navigation",
        [
            "Credit Scoring",
            "Dashboard",
            "Model Performance",
            "System Modules",
            "Portfolio Monitoring",
            "Methodology",
        ],
    )

    st.divider()

    st.markdown("**Outputs**")
    st.write("• Credit Score")
    st.write("• Repayment Risk")
    st.write("• Approve / Review / Decline")

    st.divider()

    st.markdown("**Active model**")
    st.success("Balanced Logistic Regression")

    st.markdown("**Software layers**")
    st.write("• Streamlit UI")
    st.write("• FastAPI backend")
    st.write("• ML prediction module")


if page == "Credit Scoring":
    render_credit_scoring()

elif page == "Dashboard":
    render_dashboard()

elif page == "Model Performance":
    render_model_performance()

elif page == "System Modules":
    render_system_modules()

elif page == "Portfolio Monitoring":
    render_portfolio_monitoring()

elif page == "Methodology":
    render_methodology()




