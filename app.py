import streamlit as st
import joblib
import pandas as pd
import numpy as np

# 1. Modeli ve Sütunları Yükle
model = joblib.load('student_test_xgb_model.pkl')
model_columns = model.get_booster().feature_names

st.title("🎓 Öğrenci Başarı Analizi")

# --- KULLANICI GİRİŞLERİ ---
with st.sidebar:
    st.header("📋 Öğrenci Bilgileri")
    age = st.slider("Yaş", 15, 30, 20)
    gender = st.selectbox("Cinsiyet", ["Male", "Female", "Other"])
    internet = st.radio("İnternet Erişimi", ["Yes", "No"])

col1, col2 = st.columns(2)

with col1:
    study_hours = st.number_input("Günlük Çalışma Saati", 0.0, 24.0, 6.0)
    attendance = st.slider("Derse Katılım (%)", 0, 100, 85)
    sleep_hours = st.number_input("Uyku Saati", 0.0, 15.0, 7.5)
    sleep_quality = st.select_slider("Uyku Kalitesi", options=["Poor", "Average", "Good"])

with col2:
    course = st.selectbox("Bölüm", ["B.Tech", "BCA", "B.Com", "B.Sc", "BA", "BBA", "Diploma"])
    method = st.selectbox("Çalışma Yöntemi", ["Coaching", "Self-Study", "Group Study", "Mixed", "Online Videos"])
    facility = st.selectbox("Okul İmkanları", ["Low", "Medium", "High"])
    difficulty = st.selectbox("Sınav Zorluk Algısı", [0, 1, 2], format_func=lambda x: ["Kolay", "Orta", "Zor"][x])

# --- HESAPLAMA VE TAHMİN ---
if st.button("Analizi Çalıştır"):
    # 69-71 sütunlu boş tablo oluştur (Hangi sürümü eğittiysen o genişlikte)
    girdi_df = pd.DataFrame(0.0, index=[0], columns=model_columns)
    
    # Sayısal Değerler
    girdi_df['age'] = age
    girdi_df['study_hours'] = study_hours
    girdi_df['class_attendance'] = attendance
    girdi_df['sleep_hours'] = sleep_hours
    girdi_df['exam_difficulty'] = difficulty
    
    # Mapping (Sayıya çevirme)
    sleep_map = {"Poor": 1, "Average": 2, "Good": 3}
    girdi_df['sleep_quality_numeric'] = sleep_map[sleep_quality]
    
    # Senin Meşhur Feature Engineering Formüllerin!
    girdi_df['Total_Effort'] = study_hours + (attendance / 10.0)
    girdi_df['study_hours_sq'] = study_hours ** 2
    girdi_df['attendance_sq'] = attendance ** 2
    girdi_df['Rest_Quality_Index'] = sleep_hours * sleep_map[sleep_quality]
    girdi_df['Study_Per_Attendance'] = study_hours / (attendance + 1.0)
    
    # One-Hot Encoding (bool sütunları doldurma)
    # 1. Cinsiyet, İnternet, Uyku, Tesis
    def set_bool(col_prefix, value):
        col_name = f"{col_prefix}_{value.lower()}"
        if col_name in girdi_df.columns:
            girdi_df[col_name] = 1.0

    set_bool("gender", gender)
    set_bool("internet_access", internet)
    set_bool("sleep_quality", sleep_quality)
    set_bool("facility_rating", facility)
    set_bool("course", course)
    set_bool("study_method", method)

    # 2. KRİTİK: Course_Method_Match (Örn: Course_Method_Match_b.tech_coaching)
    match_col = f"Course_Method_Match_{course.lower()}_{method.lower()}"
    if match_col in girdi_df.columns:
        girdi_df[match_col] = 1.0

    # Tahmin
    tahmin = model.predict(girdi_df)[0]
    
    # Sonuç Ekranı
    st.divider()
    st.balloons()
    st.success(f"### Tahmini Sınav Puanı: {tahmin:.2f}")