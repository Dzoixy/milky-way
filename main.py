from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from src.model import DiabetesAI
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

ai_engine = DiabetesAI()

class HealthInput(BaseModel):
    weight: float
    height: float
    waist: float
    glucose: float # รับค่า 0 หากผู้ใช้ไม่ทราบผล
    age: int
    family_history: float = 0.5

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict_risk(data: HealthInput):
    # Strategic Screening: หากไม่ทราบค่าน้ำตาล ให้ใช้ค่าฐานที่ 100 mg/dL
    actual_glucose = data.glucose if data.glucose > 0 else 100.0
    
    height_m = data.height / 100
    bmi = round(data.weight / (height_m ** 2), 2)
    wthr = round(data.waist / data.height, 2)
    
    # AI-Powered Screening ประมวลผล 8 Features
    features = [0, actual_glucose, 80, 20, 0, bmi, data.family_history, data.age]
    risk_prob = ai_engine.predict_proba(features)
    risk_percent = round(risk_prob * 100, 2)

    # Tailored Advice Engine ตามเค้าโครงนวัตกรรม
    if data.glucose <= 0 and risk_percent > 50:
        advice = "⚠️ AI พบความเสี่ยง: แนะนำให้เภสัชกรทำการตรวจน้ำตาลที่ปลายนิ้ว (POCT) ทันที"
    elif risk_percent > 70:
        advice = "🔴 ความเสี่ยงสูง: แนะนำส่งต่อโรงพยาบาลเครือข่ายเพื่อรับการวินิจฉัย"
    elif risk_percent > 30:
        advice = "🟡 ความเสี่ยงปานกลาง: ควรปรับพฤติกรรมการบริโภคและออกกำลังกาย"
    else:
        advice = "🟢 ความเสี่ยงต่ำ: รักษาสุขภาพและตรวจเช็คประจำปี"

    return {
        "risk_percent": risk_percent,
        "bmi": bmi,
        "wthr": wthr,
        "advice": advice
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)