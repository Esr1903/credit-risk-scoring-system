from fastapi import FastAPI
from src.predict import predict_credit_risk
from api.schemas import CreditRiskInput, CreditRiskOutput

app = FastAPI(
    title="Credit Risk Scoring API",
    description="South German Credit veri seti ile geliştirilen kredi risk tahmin API servisi.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Credit Risk Scoring API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Credit Risk API is running"
    }

@app.post("/predict", response_model=CreditRiskOutput)
def predict(customer_data: CreditRiskInput):
    customer_dict = customer_data.model_dump()
    result = predict_credit_risk(customer_dict)
    return result
