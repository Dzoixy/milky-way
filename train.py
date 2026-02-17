import pandas as pd
import os # เพิ่มการ import os
from src.model import DiabetesAI

def run_training():
    # 1. โหลดข้อมูล (ปรับให้รองรับ Path บน Cloud)
    # ใช้ os.path.join เพื่อให้ Path ถูกต้องทั้งบน Windows และ Linux
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'raw', 'diabetes.csv')
    
    try:
        df = pd.read_csv(data_path)
        print(f"✅ Load data successfully from: {data_path}")
    except FileNotFoundError:
        # ลองหาในโฟลเดอร์ปัจจุบันเผื่อกรณี Docker ทำงานอยู่ที่ /app
        alternative_path = 'data/raw/diabetes.csv'
        try:
            df = pd.read_csv(alternative_path)
            print(f"✅ Load data successfully from alternative path!")
        except:
            print(f"❌ Error: ไม่พบไฟล์ข้อมูลใน {data_path}")
            return

    # 2. สร้าง instance และ 3. เทรน Model (เหมือนเดิม)
    ai_engine = DiabetesAI()
    status = ai_engine.train(df)
    print(f"🤖 AI {status}")

if __name__ == "__main__":
    run_training()