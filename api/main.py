from fastapi import FastAPI


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