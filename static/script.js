// src/static/script.js

// ฟังก์ชันเปิด/ปิดช่องกรอกน้ำตาล
function toggleGlucose() {
    const isUnknown = document.getElementById('unknown_glucose').checked;
    const glucoseInput = document.getElementById('glucose');
    
    if (isUnknown) {
        glucoseInput.value = '';
        glucoseInput.disabled = true;
        glucoseInput.placeholder = "ใช้ AI ประเมินจากรูปร่าง";
    } else {
        glucoseInput.disabled = false;
        glucoseInput.placeholder = "100";
    }
}

// ฟังก์ชันส่งข้อมูลไป Backend
async function analyzeRisk() {
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);
    const waist = parseFloat(document.getElementById('waist').value);
    const age = parseInt(document.getElementById('age').value);
    
    // จัดการค่าน้ำตาล
    let glucose = 0;
    if (!document.getElementById('unknown_glucose').checked) {
        glucose = parseFloat(document.getElementById('glucose').value);
    }

    // Validation เบื้องต้น
    if (!weight || !height || !waist || !age) {
        alert("กรุณากรอกข้อมูลสัดส่วนร่างกายให้ครบถ้วน");
        return;
    }

    const payload = {
        weight: weight,
        height: height,
        waist: waist,
        glucose: glucose ? glucose : 0,
        age: age
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        displayResult(result);

    } catch (error) {
        console.error('Error:', error);
        alert('เกิดข้อผิดพลาดในการเชื่อมต่อระบบ');
    }
}

function displayResult(data) {
    const resultArea = document.getElementById('resultArea');
    const scoreVal = document.getElementById('scoreVal');
    const messageBox = document.getElementById('resultMessage');
    
    // Reset classes
    resultArea.className = 'result-visible status-' + data.action_type;
    
    // Set Data
    scoreVal.innerText = data.risk_score;
    messageBox.innerHTML = data.message;
    document.getElementById('bmiVal').innerText = data.bmi;
    document.getElementById('wthrVal').innerText = data.wthr;

    // Scroll to result
    resultArea.scrollIntoView({ behavior: 'smooth' });
}