# File: api_server.py

import os
import sys
import requests
from flask import Flask, request, jsonify

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Gemini Configuration ---
# Load your secret API key from an environment variable for security.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-1.5-flash-latest"
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}'

def get_analysis_from_gemini(html_content, payload):
    """
    This function lives on the server and securely calls the Gemini API.
    """
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable not set on the server.")
        return "ERROR: Analysis server is not configured correctly."

    truncated_response = html_content[:30000]

    prompt = f"""
        You are a web security expert. Analyze the following for a Reflected XSS vulnerability.
        
        **Injected Payload:** `{payload}`
        **Resulting HTML Response (partial):**
        ```html
        {truncated_response}
        ```
        **Your Task:**
        Respond with a single line starting with "VULNERABLE:" or "SAFE:".
        - If VULNERABLE, explain where it's reflected. Example: "VULNERABLE: Reflected inside an HTML attribute without encoding."
        - If SAFE, explain why. Example: "SAFE: Payload is properly HTML-encoded."
    """
    headers = {'Content-Type': 'application/json'}
    data = {'contents': [{'parts': [{'text': prompt}]}]}

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data, timeout=25)
        response.raise_for_status()
        result = response.json()
        if 'candidates' in result and result['candidates']:
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        return "SAFE: Gemini response was empty."
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return "ERROR: Could not get analysis from the AI."

@app.route('/analyze', methods=['POST'])
def handle_analysis_request():
    """
    This is the public endpoint that the xsspy tool will call.
    """
    request_data = request.get_json()
    if not request_data or 'html_content' not in request_data or 'payload' not in request_data:
        return jsonify({'error': 'Invalid request. Missing html_content or payload.'}), 400

    html_content = request_data['html_content']
    payload = request_data['payload']
    analysis_result = get_analysis_from_gemini(html_content, payload)
    return jsonify({'analysis': analysis_result})

if __name__ == '__main__':
    # This block is for local testing. Render uses the gunicorn command instead.
    if not GEMINI_API_KEY:
        print("\n[FATAL ERROR] The GEMINI_API_KEY is not set.")
        print("Please set the environment variable before running the server locally.")
        sys.exit(1)
    
    app.run(host='0.0.0.0', port=5000)
