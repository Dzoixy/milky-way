function toggleGlucose(checkbox) {
    const input = document.getElementById('glucose');
    input.disabled = checkbox.checked;
    if(checkbox.checked) input.value = "";
}

async function checkRisk() {
    const isNoGlucose = document.getElementById('no_glucose').checked;
    const data = {
        weight: parseFloat(document.getElementById('weight').value),
        height: parseFloat(document.getElementById('height').value),
        waist: parseFloat(document.getElementById('waist').value),
        glucose: isNoGlucose ? 0 : parseFloat(document.getElementById('glucose').value),
        age: parseInt(document.getElementById('age').value)
    };

    if(!data.weight || !data.height || !data.waist) {
        alert("กรุณากรอกข้อมูลสัดส่วนร่างกายให้ครบถ้วนเพื่อความแม่นยำสูง");
        return;
    }

    const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    const resBox = document.getElementById('result-box');
    const resText = document.getElementById('result-text');

    resBox.className = 'result-box'; // Reset
    resText.innerHTML = `
        <div style="font-size: 0.8rem; opacity: 0.9; margin-bottom: 5px;">ผลวิเคราะห์ระดับบุคคล (N=1)</div>
        <div style="font-size: 1.4rem; font-weight: 800;">ความเสี่ยง ${result.risk_percent}%</div>
        <div style="font-size: 0.85rem; margin: 10px 0;">BMI: ${result.bmi} | WtHR: ${result.wthr}</div>
        <div style="font-size: 0.95rem; font-weight: 600; padding: 10px; background: rgba(0,0,0,0.1); border-radius: 10px;">${result.advice}</div>
    `;

    resBox.style.display = 'block';
    if (result.risk_percent > 70) resBox.classList.add('risk-high');
    else if (result.risk_percent > 30) resBox.classList.add('risk-med');
    else resBox.classList.add('risk-low');
}