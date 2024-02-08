from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
import os
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def extract_text_between_brackets(text):
    # Define the regular expression pattern to match text between brackets and last full stop
    pattern = r'\[SEP\](.*?)\.'

    # Find all matches using the pattern
    matches = re.findall(pattern, text, re.DOTALL)

    # If there are matches, return the last match
    if matches:
        return matches[-1].strip()
    else:
        return None
    

@app.route('/generate-text', methods=['POST'])
def generate_text():
    input_text = request.json.get('text')
    response = requests.post(
        "https://api-inference.huggingface.co/models/AngeloMakory/UzimaBot",
        headers={"Authorization": "Bearer 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"},
        json={"inputs": input_text, "parameters": {"max_length": 50}}
    )
    if response.status_code == 200:
        res = response.json()[0]['generated_text']
        return jsonify(extract_text_between_brackets(res))
    
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
