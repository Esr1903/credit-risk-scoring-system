import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.predict import predict_credit_risk

#bilerek eksik müşteri verisi oluşturuyorum
incomplete_customer = {
    "status": 1,
    "duration": 24,
    "amount": 3000
}

#tahmin yapmayı deniyelim
try:
    result = predict_credit_risk(incomplete_customer)
    print("Tahmin sonucu:")
    print(result)
#Eğer eksik veri yüzünden hata oluşursa bu bölüm çalışsın
except ValueError as error:
    print("Validation hatası yakalandı.")
    print(error)