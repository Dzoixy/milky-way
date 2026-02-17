import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

class DiabetesAI:
    def __init__(self, model_path='model/diabetes_model.pkl'):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        # ตรวจสอบว่ามีไฟล์ model หรือยัง
        if os.path.exists(self.model_path):
            return joblib.load(self.model_path)
        # ถ้าไม่มี ให้เตรียมโครงสร้าง Model ไว้ (รอการ Train)
        return RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, df):
        # สมมติว่าไฟล์ CSV มีคอลัมน์ 'Outcome' เป็นเป้าหมาย
        X = df.drop('Outcome', axis=1)
        y = df['Outcome']
        self.model.fit(X, y)
        
        # สร้างโฟลเดอร์ถ้ายังไม่มี
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        return "Training Success!"

    def predict_proba(self, features):
        """
        features: list ของค่าสุขภาพ เช่น [Pregnancies, Glucose, BloodPressure, ...]
        """
        # ทายผลเป็นความน่าจะเป็น (Probability) เพื่อใช้จัดกลุ่ม เสี่ยงต่ำ/กลาง/สูง
        prob = self.model.predict_proba([features])[0][1]
        return prob