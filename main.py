# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.model import DiabetesAI # เรียกใช้ Logic จากไฟล์ model
import uvicorn
import os

app = FastAPI()

# Mount โฟลเดอร์ static เพื่อให้เรียกใช้ css/js ได้
app.mount("/static", StaticFiles(directory="static"), name="static")
# เริ่มต้น AI Engine
ai_engine = DiabetesAI()

# รูปแบบข้อมูลที่รับจากหน้าบ้าน
class HealthInput(BaseModel):
    weight: float
    height: float
    waist: float
    glucose: float
    age: int

# Route หลัก: เปิดหน้าเว็บ (ดึงไฟล์จาก src/static/index.html)
@app.get("/")
async def read_index():
    return FileResponse('src/static/index.html')

# API สำหรับคำนวณ
@app.post("/predict")
async def predict_risk(data: HealthInput):
    result = ai_engine.predict_risk(data)
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)