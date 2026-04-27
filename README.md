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