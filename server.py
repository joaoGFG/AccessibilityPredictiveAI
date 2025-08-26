from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

model = joblib.load("./model/assistencia_model.pkl")

# Lógica por trás da transformação dos dados de entrada com bin map
def preprocess_input(data):
    bin_map = {
        "sim": 1,
        "não": 0,
        "nao": 0,
        "Sim": 1,
        "Não": 0,
        "Nao": 0
    }

    sexo_map = {
        "M": 0,
        "F": 1
    }

    linha_metro_map = {
        "Azul": 0,
        "Verde": 1,
        "Vermelha": 2,
        "Amarela": 3,
    }

    return {
        "idade": int(data.get("idade", 0)),
        "sexo": sexo_map.get(data.get("sexo", "M"), 0),
        "linha_metro": linha_metro_map.get(data.get("linha_metro", "Azul"), 0),
        "estacao_movimentada": bin_map.get(data.get("estacao_movimentada", "nao"), 0),
        "usa_bengala": bin_map.get(data.get("usa_bengala", "nao"), 0),
        "aplicativo_acessibilidade": bin_map.get(data.get("aplicativo_acessibilidade", "nao"), 0),
        "horario_pico": bin_map.get(data.get("horario_pico", "nao"), 0),
        "usa_cao_guia": bin_map.get(data.get("usa_cao_guia", "nao"), 0),
        "tempo_de_espera": int(data.get("tempo_de_espera", 0))
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("📥 Dados recebidos:", data)
        processed_data = preprocess_input(data)
        df = pd.DataFrame([processed_data])
        print("🧾 Dados processados:", df)
        prediction = model.predict(df)[0]
        if prediction >= 0.7:
            return jsonify({"prediction": "Precisa de assistência"})
        else:
            return jsonify({"prediction": "Não precisa de assistência"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
