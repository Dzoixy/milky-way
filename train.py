import pandas as pd
from src.model import DiabetesAI  # ใช้ Class OOP ที่เราเขียนไว้

def run_training():
    # 1. โหลดข้อมูล
    data_path = 'data/raw/diabetes.csv'
    try:
        df = pd.read_csv(data_path)
        print("✅ Load data successfully!")
    except FileNotFoundError:
        print("❌ Error: ไม่พบไฟล์ข้อมูลใน data/raw/")
        return

    # 2. สร้าง instance ของ AI Engine
    ai_engine = DiabetesAI()

    # 3. เทรน Model
    # หมายเหตุ: ในชุดข้อมูล Pima คอลัมน์เป้าหมายชื่อ 'Outcome'
    status = ai_engine.train(df)
    print(f"🤖 AI {status}")

if __name__ == "__main__":
    run_training()