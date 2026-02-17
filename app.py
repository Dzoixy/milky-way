import streamlit as st
import pandas as pd
from src.model import DiabetesAI
from src.utils import calculate_bmi

# เรียกใช้ Class ที่เราเขียนไว้
ai_engine = DiabetesAI()

st.set_page_config(page_title="Milky-Way AI", layout="wide")
st.title("🌌 Milky-Way: Precision Diabetes Screening")

# ส่วนรับข้อมูลจากผู้ใช้
with st.container():
    st.subheader("📝 ข้อมูลสุขภาพเบื้องต้น")
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("น้ำหนัก (kg)", value=65.0)
        height = st.number_input("ส่วนสูง (cm)", value=170.0)
    with col2:
        age = st.slider("อายุ", 1, 100, 25)
        glucose = st.number_input("ระดับน้ำตาลในเลือด (ถ้ามี)", value=90)

if st.button("วิเคราะห์ความเสี่ยงด้วย AI"):
    bmi = calculate_bmi(weight, height)
    # สมมติลำดับ features ตามที่ Model ถูกเทรนมา
    # ตัวอย่าง: [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
    dummy_features = [0, glucose, 80, 20, 0, bmi, 0.5, age]
    
    risk_prob = ai_engine.predict(dummy_features)
    
    # แสดงผลตามระดับความเสี่ยง
    if risk_prob > 0.7:
        st.error(f"🔴 ความเสี่ยงสูง ({risk_prob:.2%}): แนะนำให้พบเภสัชกรเพื่อตรวจยืนยัน")
    elif risk_prob > 0.3:
        st.warning(f"🟡 ความเสี่ยงปานกลาง ({risk_prob:.2%}): ควรปรับพฤติกรรมการบริโภค")
    else:
        st.success(f"🟢 ความเสี่ยงต่ำ ({risk_prob:.2%}): สุขภาพอยู่ในเกณฑ์ดี")