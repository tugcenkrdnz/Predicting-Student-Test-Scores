# Kaggle Playground S6E1 - 🎓 Predicting Student Test Scores (Öğrenci Sınav Puanı Tahminleme)

Bu proje, Kaggle Playground Series S6E1 kapsamında hazırlanan, öğrencilerin akademik alışkanlıkları ve demografik bilgilerine dayanarak sınav puanlarını tahmin eden bir uçtan uca makine öğrenmesi çözümüdür.

## 🚀 Başarı Metrikleri
- **Model:** XGBRegressor (Şampiyon Model)
- **R² Skoru:** 0.7268
- **RMSE** 8.7488
- **MAE** 6.9728

## 🧠 Özellik Mühendisliği (Feature Engineering)
Projenin başarısındaki en büyük pay, veriden türetilen özel değişkenlere aittir:
- **Total_Effort:** `study_hours + (attendance / 10)` formülüyle öğrencinin toplam gayreti ölçülmüştür (Önem derecesi: %41).
- **Rest_Quality_Index:** Uyku saati ve kalitesinin etkileşimi.
- **Course_Method_Match:** Bölüm ve çalışma yöntemi arasındaki sinerjiyi ölçen etkileşim değişkenleri.
- **Karesel Özellikler:** `study_hours_sq` gibi değişkenlerle doğrusal olmayan ilişkiler yakalanmıştır.

## 🛠️ Kullanılan Teknolojiler
- **Donanım:** Apple M4 MacBook Pro
- **Kütüphaneler:** Python, XGBoost, Scikit-learn, Pandas, Streamlit


## 💻 Uygulamayı Çalıştırma
Uygulama Streamlit üzerinden web arayüzü ile sunulmaktadır. Yerelde çalıştırmak için:

```bash
pip install -r requirements.txt
streamlit run app.py