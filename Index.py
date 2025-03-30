from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")
URL = os.getenv("URL")

url_com_chave = f'{URL}?key={API_KEY}'

HEADERS = {
    "Content-Type": "application/json"
}

@app.route('/api/generate_quests', methods=['POST'])
def main():
    data = request.get_json()

    # Validação dos dados recebidos
    if not data or "context" not in data or "quantidade_tasks" not in data:
        return jsonify({"error": "Os campos 'context' e 'quantidade_tasks' são obrigatórios"}), 400  

    context = data["context"]
    quantidade_tasks = data["quantidade_tasks"]

    prompt = (
        f"Crie exatamente {quantidade_tasks} perguntas e respostas sobre: {context}. "
        "Cada pergunta deve terminar com '?' e a resposta deve ser um texto conciso logo abaixo. "
        "Não inclua nenhuma introdução ou explicação, apenas as perguntas e respostas."
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url_com_chave, json=payload, headers=HEADERS)

    if response.status_code == 200:
        json_response = response.json()

        try:
            # Pegando a resposta gerada pela IA
            text = json_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

            if not text:
                return jsonify({"error": "A resposta da IA veio vazia."}), 500

            # Regex para identificar perguntas e respostas
            pattern = re.findall(r"(.+?\?)\s*(.+?)(?=\n\n|\Z)", text, re.DOTALL)

            flashcards = []
            for pergunta, resposta in pattern:
                flashcards.append({
                    "frente": pergunta.strip(),
                    "verso": resposta.strip()
                })

            if not flashcards:
                return jsonify({"error": "Não foi possível extrair perguntas e respostas corretamente."}), 500

        except json.JSONDecodeError:
            return jsonify({"error": "Erro ao converter resposta da IA para JSON. O formato pode estar incorreto."}), 500
        except KeyError:
            return jsonify({"error": "Erro ao acessar a resposta da IA. Estrutura inesperada."}), 500

    else:
        return jsonify({"error": f"Erro {response.status_code}: {response.text}"}), 500

    return jsonify({
        "message": "Ok",
        "flashcards": flashcards
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
