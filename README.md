# Credit Risk Scoring System

Bu proje, South German Credit veri seti kullanılarak geliştirilmiş bir kredi risk tahmin sistemidir.

Amaç, müşteri bilgilerine göre kredi riskini tahmin etmek, kötü kredi olasılığını hesaplamak, model tabanlı bir kredi skoru üretmek ve kredi başvurusu için karar önerisi sunmaktır.

## Proje Amacı

Bu sistem, kredi başvurusu yapan bir müşterinin geri ödeme riskini tahmin eder.

Model çıktıları:

- Kötü kredi olasılığı
- İyi kredi olasılığı
- Model tabanlı kredi skoru
- Risk bandı
- Karar önerisi

Karar önerileri:

- APPROVE
- REVIEW
- DECLINE

## Veri Seti

Projede South German Credit veri seti kullanılmıştır.

Temizlenmiş veri dosyası:

```text
data/processed/south_german_credit_clean.csv
```

Hedef değişken:

```text
credit_risk
0 = kötü kredi
1 = iyi kredi
```

Veri seti özeti:

```text
1000 satır
20 özellik
1 hedef değişken
```

## Kullanılan Model

Final model adayı olarak Balanced Logistic Regression seçilmiştir.

Model dosyası:

```text
models/balanced_logistic_regression.pkl
```

Bu model pipeline olarak kaydedilmiştir. Yani model dosyası hem preprocessing adımlarını hem de Logistic Regression modelini içerir.

## Tahmin Çıktısı Örneği

Örnek çıktı:

```text
=== Credit Risk Prediction Result ===

Prediction Label: Kötü kredi riski
Bad Credit Probability: 68.3%
Good Credit Probability: 31.7%
Credit Score: 474 / 850
Decision: DECLINE
Risk Band: High Risk
```

## Karar Mantığı

Model önce kötü kredi olasılığını üretir.

Bu olasılık daha sonra 300–850 aralığında model tabanlı kredi skoruna dönüştürülür.

Kredi skoru formülü:

```text
credit_score = 300 + (1 - bad_credit_probability) * 550
```

Karar eşikleri:

```text
bad_credit_probability < 0.25 -> APPROVE
0.25 <= bad_credit_probability < 0.55 -> REVIEW
bad_credit_probability >= 0.55 -> DECLINE
```

Risk bandı eşikleri:

```text
bad_credit_probability < 0.25 -> Low Risk
0.25 <= bad_credit_probability < 0.55 -> Medium Risk
bad_credit_probability >= 0.55 -> High Risk
```

## Örnek Müşteri Verisi

Manuel tahmin testinde kullanılan örnek müşteri verisi ayrı bir JSON dosyasında tutulur.

Dosya yolu:

```text
data/sample/sample_customer.json
```

Bu dosya, tek bir müşteri başvurusuna ait örnek input değerlerini içerir.

Manuel tahmin testi çalıştırıldığında `tests/test_predict_manual.py` dosyası bu JSON dosyasını okur ve `predict_credit_risk()` fonksiyonuna gönderir.

## Streamlit Dashboard Kullanımı

Projede kullanıcı dostu bir Streamlit tabanlı FinTech kredi skorlama dashboard'u bulunmaktadır.

Dashboard dosyası:

```text
app/streamlit_app.py
```

Streamlit uygulamasını çalıştırmak için:

```powershell
streamlit run app/streamlit_app.py
```

Uygulama açıldığında tarayıcıda genellikle şu adresten erişilebilir:

```text
http://localhost:8501
```

Dashboard üzerinden kullanıcı müşteri başvuru bilgilerini girerek kredi risk tahmini alabilir.

Dashboard çıktıları:

```text
Credit Score
Repayment Risk
APPROVE / REVIEW / DECLINE kararı
Risk Band
Bad Credit Probability
Good Credit Probability
AI Decision Explanation
Risk Signals
Positive Signals
```

Dashboard menüleri:

```text
Credit Scoring
Dashboard
Model Performance
System Modules
Portfolio Monitoring
Methodology
```

### Credit Scoring

Kullanıcının müşteri başvuru bilgilerini girdiği ana ekrandır.

Bu ekranda kullanıcı:

```text
Applicant name
Credit duration
Credit amount
Age
Checking account status
Credit history
Savings level
Employment duration
Housing
Job type
```

gibi bilgileri girer.

Sonra şu butona basar:

```text
Analyze Credit Risk
```

Sistem model üzerinden kredi riskini tahmin eder ve aşağıdaki çıktıları üretir:

```text
Credit Score
Recommended Decision
Risk Band
Bad Risk
Good Credit
```

### Model Performance

Bu ekran model performans analizini gösterir.

Gösterilen metrikler:

```text
Accuracy
Bad Credit Recall
Model comparison
Selected model
```

Final model olarak Balanced Logistic Regression kullanılmıştır.

Bu model, kötü kredi riskini yakalama performansı dikkate alınarak seçilmiştir. Çünkü kredi risk problemlerinde riskli müşteriyi güvenli müşteri olarak sınıflandırmak finansal açıdan daha maliyetli olabilir.

### System Modules

Bu ekran, modern bir AI kredi risk sisteminde bulunması gereken modülleri gösterir:

```text
Data Ingestion & Unification
Real-Time Scoring Engine
Explainable Dashboard
Portfolio Monitoring
Compliance & Reporting
Integration APIs
```

Bu proje kapsamında bazı modüller aktif olarak uygulanmış, bazıları ise prototip veya gelecek geliştirme alanı olarak gösterilmiştir.

### Portfolio Monitoring

Bu ekran, kredi portföyündeki müşterilerin risk dağılımını izlemek için prototip bir görünüm sunar.

Gösterilen bilgiler:

```text
Low Risk Accounts
Review Queue
High Risk Alerts
Portfolio Decision Distribution
```

### Methodology

Bu ekran projenin teknik açıklamasını içerir:

```text
Dataset
Target variable
Model
Credit score formula
Decision thresholds
Limitations
Production requirements
```



## API Kullanımı

Projede FastAPI ile geliştirilmiş basit bir API katmanı bulunmaktadır.

API dosyası:

```text
api/main.py
```

Mevcut endpointler:

```text
GET /
GET /health
POST /predict
```

API sunucusunu başlatmak için:

```powershell
uvicorn api.main:app --reload
```

Sunucu çalıştıktan sonra FastAPI dokümantasyon ekranı şu adresten açılabilir:

```text
http://127.0.0.1:8000/docs
```

Health kontrolü için:

```text
http://127.0.0.1:8000/health
```

Beklenen cevap:

```json
{
  "status": "ok",
  "message": "Credit Risk API is running"
}
```

Model tahmini için `POST /predict` endpoint'i kullanılır.

Örnek input:

```json
{
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
```

Örnek output:

```json
{
  "prediction": 0,
  "prediction_label": "Kötü kredi riski",
  "bad_credit_probability": 0.683,
  "good_credit_probability": 0.317,
  "credit_score": 474,
  "decision": "DECLINE",
  "risk_band": "High Risk"
}
```

API endpointlerini manuel test etmek için önce API sunucusu çalıştırılmalıdır:

```powershell
uvicorn api.main:app --reload
```

Sonra ayrı bir terminalden şu komut çalıştırılabilir:

```powershell
python tests/test_api_manual.py
```


## Manuel Test Komutları

Tahmin fonksiyonunu örnek müşteriyle test etmek için:

```powershell
python tests/test_predict_manual.py
```

Eksik müşteri verisi validation testini çalıştırmak için:

```powershell
python tests/test_validation_manual.py
```

## Önemli Dosyalar

```text
src/predict.py
```

Tahmin fonksiyonlarını, kredi skoru hesaplamasını, karar motorunu ve input validation kontrolünü içerir.

```text
tests/test_predict_manual.py
```

Örnek müşteriyle manuel tahmin testi yapar.

```text
tests/test_validation_manual.py
```

Eksik müşteri bilgisi durumunda validation kontrolünü test eder.

```text
data/sample/sample_customer.json
```

Manuel tahmin testinde kullanılan örnek müşteri verisini içerir.

```text
models/balanced_logistic_regression.pkl
```

Kaydedilmiş final model pipeline dosyasıdır.

## Proje Durumu

Tamamlanan ana bileşenler:

- Veri temizleme
- EDA çalışmaları
- Modelleme hazırlığı
- Logistic Regression modeli
- Decision Tree modeli
- Random Forest modeli
- Balanced Logistic Regression modeli
- Final model kaydetme
- Tek müşteri tahmini
- Tahmin fonksiyonunu `src` klasörüne taşıma
- Kredi skoru ve karar motoru
- Input validation
- Manuel test dosyaları
- Örnek müşteri JSON dosyası
- Başlangıç README dokümantasyonu

Gelecek aşamalar:

- FastAPI servis katmanı
- Streamlit kullanıcı arayüzü
- Batch prediction
- Model performans ekranı
- Final rapor