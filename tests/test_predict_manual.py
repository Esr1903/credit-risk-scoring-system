#src/predict.py içindeki predict_credit_risk fonksiyonunu örnek müşteriyle kolayca test etmek.
''' Bu dosya sadece:
fonksiyon doğru çalışıyor mu?
jsondaki örnek müşteri için çıktı geliyor mu? diye kontrol etmek için.   '''
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.predict import predict_credit_risk

"""sample_customer.json dosyasının yolunu bul.
Dosyayı oku.
İçindeki JSON verisini Python sözlüğüne çevir.
Bu sözlüğü sample_customer değişkenine ata."""
sample_customer_path = PROJECT_ROOT / "data" / "sample" / "sample_customer.json"

with open(sample_customer_path, "r", encoding="utf-8") as file:
    sample_customer = json.load(file)



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
