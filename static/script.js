document.getElementById('predict-form').addEventListener('submit', async function(e) {
  e.preventDefault(); 

  const formData = new FormData(e.target);
  const data = {};
  formData.forEach((value, key) => data[key] = value);

  const response = await fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  if ('prediction' in result) {
    document.getElementById('resultado').innerText = `Previsão: ${result.prediction}`;
  } else {
    document.getElementById('resultado').innerText = `Erro: ${result.error}`;
  }
});

