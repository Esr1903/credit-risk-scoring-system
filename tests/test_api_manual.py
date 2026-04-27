import json
from pathlib import Path

import requests


API_BASE_URL = "http://127.0.0.1:8000"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_CUSTOMER_PATH = PROJECT_ROOT / "data" / "sample" / "sample_customer.json"


print("=== API Manual Test ===")
print()

print("1. Health endpoint test ediliyor...")
health_response = requests.get(f"{API_BASE_URL}/health")

print("Status code:", health_response.status_code)
print("Response:", health_response.json())
print()

print("2. Predict endpoint test ediliyor...")

with open(SAMPLE_CUSTOMER_PATH, "r", encoding="utf-8") as file:
    sample_customer = json.load(file)

predict_response = requests.post(
    f"{API_BASE_URL}/predict",
    json=sample_customer
)

print("Status code:", predict_response.status_code)
print("Response:", predict_response.json())