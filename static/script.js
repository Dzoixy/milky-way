async function checkRisk() {
    const data = {
        glucose: parseFloat(document.getElementById('glucose').value),
        bmi: parseFloat(document.getElementById('bmi').value),
        age: parseInt(document.getElementById('age').value)
    };

    const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    const resultBox = document.getElementById('result-box');
    const resultText = document.getElementById('result-text');

    resultBox.classList.remove('hidden');
    resultText.innerText = `ความเสี่ยงของคุณคือ: ${result.risk_percent}%`;
    
    // เปลี่ยนสีตามระดับความเสี่ยง
    if (result.risk_percent > 70) resultBox.style.backgroundColor = "#ff4d4d";
    else if (result.risk_percent > 30) resultBox.style.backgroundColor = "#ffa500";
    else resultBox.style.backgroundColor = "#2ecc71";
}