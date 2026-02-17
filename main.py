from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from src.model import DiabetesAI
import uvicorn

app = FastAPI()

# เชื่อมต่อโฟลเดอร์ static สำหรับไฟล์ CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

# เรียกใช้งาน AI Engine (OOP Class เดิมของน้อง)
ai_engine = DiabetesAI()

class HealthData(BaseModel):
    glucose: float
    bmi: float
    age: int

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict_risk(data: HealthData):
    # เรียงลำดับ features ให้ตรงกับที่เทรนมา (สมมติลำดับเบื้องต้น)
    features = [0, data.glucose, 80, 20, 0, data.bmi, 0.5, data.age]
    risk_prob = ai_engine.predict_proba(features)
    return {"risk_percent": round(risk_prob * 100, 2)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)