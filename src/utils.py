import asyncio

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 2)

async def fetch_sensor_data():
    # จำลองการดึงข้อมูลจาก ESP32/Sensor ผ่าน API แบบ Async
    await asyncio.sleep(1) # จำลอง Network Latency
    return {"temp": 36.5, "status": "connected"}