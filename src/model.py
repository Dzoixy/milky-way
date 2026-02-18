# src/model.py
import os
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

class DiabetesAI:
    def __init__(self):
        # กำหนด path สำหรับบันทึกโมเดล
        self.model_dir = "model"
        self.model_path = os.path.join(self.model_dir, "diabetes_model.pkl")
        self.model = None
        
        # สร้างโฟลเดอร์ model ถ้ายังไม่มี
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
            
        # ลองโหลดโมเดลถ้ามีไฟล์อยู่แล้ว
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("✅ Model loaded successfully.")
            except Exception as e:
                print(f"⚠️ Error loading model: {e}")

    def train(self, df):
        """
        ฟังก์ชันสำหรับเทรนโมเดล (ถูกเรียกโดย train.py)
        """
        print("🧠 Start Training...")
        
        try:
            # Prepare Data (Mapping ตาม Pima Dataset)
            # X = Features, y = Outcome
            X = df.drop('Outcome', axis=1)
            y = df['Outcome']
            
            # Split & Train (ใช้ Logistic Regression เบื้องต้น)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            clf = LogisticRegression(max_iter=1000)
            clf.fit(X_train, y_train)
            
            # Save Model
            with open(self.model_path, 'wb') as f:
                pickle.dump(clf, f)
            
            self.model = clf
            print("🎉 Training Complete & Saved!")
            return True
            
        except Exception as e:
            print(f"❌ Training Failed: {e}")
            return False

    def predict_risk(self, data):
        """
        Input: data (Object) contains weight, height, waist, glucose, age
        Output: dict with risk_level, message, action_type
        """
        # 1. คำนวณค่าสัดส่วน
        height_m = data.height / 100
        if height_m == 0: height_m = 1.7
        
        bmi = round(data.weight / (height_m ** 2), 2)
        wthr = round(data.waist / data.height, 2)
        
        # 2. Strategic Logic (Rule-based เพื่อความแม่นยำในการคัดกรองเบื้องต้น)
        # เรายังใช้ Logic นี้เป็นหลัก เพราะ input หน้าเว็บอาจไม่ครบเท่า dataset ที่ใช้เทรน (เช่น ไม่มี BloodPressure)
        
        risk_score = 0
        action_type = "low"
        message = ""

        # กรณี: ไม่ทราบค่าน้ำตาล (Glucose = 0)
        if data.glucose == 0:
            if bmi > 25 or wthr > 0.55:
                risk_score = 80
                action_type = "urgent_test"
                message = f"⚠️ <b>พบความเสี่ยงจากรูปร่าง (BMI {bmi}):</b><br>AI ประเมินว่าคุณมีความเสี่ยงสูง แนะนำให้<b>ตรวจน้ำตาลปลายนิ้ว (POCT)</b> ทันที"
            elif bmi > 23 or wthr > 0.5:
                risk_score = 45
                action_type = "medium"
                message = f"🟡 <b>ความเสี่ยงปานกลาง:</b><br>รูปร่างเริ่มท้วม แนะนำคุมแป้ง/น้ำตาล และสังเกตอาการ"
            else:
                risk_score = 15
                action_type = "low"
                message = f"🟢 <b>ความเสี่ยงต่ำ:</b><br>รูปร่างสมส่วน สุขภาพดี ให้รักษามาตรฐานต่อไป"
        
        # กรณี: ทราบค่าน้ำตาลแล้ว
        else:
            if data.glucose >= 126:
                risk_score = 95
                action_type = "high"
                message = f"🔴 <b>ความเสี่ยงสูง (High Risk):</b><br>ค่าน้ำตาล {data.glucose} บ่งชี้ภาวะเบาหวาน ควรพบแพทย์"
            elif data.glucose >= 100:
                risk_score = 60
                action_type = "medium"
                message = f"🟠 <b>ภาวะก่อนเบาหวาน (Pre-Diabetes):</b><br>น้ำตาลสูงกว่าปกติ เริ่มมีความเสี่ยง"
            else:
                risk_score = 10
                action_type = "low"
                message = f"🟢 <b>ผลเลือดปกติ:</b><br>ยอดเยี่ยม! รักษาสุขภาพต่อไป"

        return {
            "bmi": bmi,
            "wthr": wthr,
            "risk_score": risk_score,
            "action_type": action_type,
            "message": message
        }