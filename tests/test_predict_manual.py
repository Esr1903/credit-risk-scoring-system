#src/predict.py içindeki predict_credit_risk fonksiyonunu örnek müşteriyle kolayca test etmek.
''' Bu dosya sadece:
fonksiyon doğru çalışıyor mu?
örnek müşteri için çıktı geliyor mu? diye kontrol etmek için.   '''

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.predict import predict_credit_risk

sample_customer = {
    "status": 1,
    "duration": 24,
    "credit_history": 2,
    "purpose": 3,
    "amount": 3000,
    "savings": 2,
    "employment_duration": 3,
    "installment_rate": 4,
    "personal_status_sex": 3,
    "other_debtors": 1,
    "present_residence": 2,
    "property": 2,
    "age": 35,
    "other_installment_plans": 3,
    "housing": 2,
    "number_credits": 1,
    "job": 3,
    "people_liable": 2,
    "telephone": 1,
    "foreign_worker": 2
}

#her alanı ayrı ayrı, daha okunabilir şekilde yazdırıyoruz.
result = predict_credit_risk(sample_customer)

print("=== Credit Risk Prediction Result ===")
print()
print(f"Prediction Label: {result['prediction_label']}")
print(f"Bad Credit Probability: {result['bad_credit_probability'] * 100:.1f}%")
print(f"Good Credit Probability: {result['good_credit_probability'] * 100:.1f}%")
print(f"Credit Score: {result['credit_score']} / 850")
print(f"Decision: {result['decision']}")
print(f"Risk Band: {result['risk_band']}")
