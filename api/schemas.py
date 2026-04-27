"""
CreditRiskInput şunu söylüyor:
/predict endpoint’i bu 20 müşteri alanını bekler.
Her alan integer olmalıdır.

CreditRiskOutput ise şunu söylüyor:
/predict endpoint’i tahmin sonucunda bu alanları döndürür.
"""

from pydantic import BaseModel


class CreditRiskInput(BaseModel):
    status: int
    duration: int
    credit_history: int
    purpose: int
    amount: int
    savings: int
    employment_duration: int
    installment_rate: int
    personal_status_sex: int
    other_debtors: int
    present_residence: int
    property: int
    age: int
    other_installment_plans: int
    housing: int
    number_credits: int
    job: int
    people_liable: int
    telephone: int
    foreign_worker: int


class CreditRiskOutput(BaseModel):
    prediction: int
    prediction_label: str
    bad_credit_probability: float
    good_credit_probability: float
    credit_score: int
    decision: str
    risk_band: str