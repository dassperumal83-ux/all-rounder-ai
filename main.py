from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Render Environment Variable la irundhu Groq key edukum - Elite security
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

@app.route('/api/knox', methods=['POST'])
def knox_reply():
    data = request.get_json()
    user_text = data.get('message', '')

    # Kelvi illama vandha
    if not user_text:
        return jsonify({
            'reply': 'Line 1: Kelvi kekala bro 💀<br>Line 2: Summa irundha AI epdi pesum? Vayiru kalla stone aagidum 😂<br>Line 3: Elite tip: Type pani anupu, naan iruken 👑'
        })

    # Key set aagala na
    if not GROQ_API_KEY:
        return jsonify({
            'reply': 'Line 1: API key set aagala bro 💀<br>Line 2: Render la GROQ_API_KEY podama epdi odum? Petrol illaama car oduma? 😂<br>Line 3: Elite tip: Environment Variables la key add panu 👑'
        })

    # KNOX ELITE personality - 3 line format
    prompt = f"""Nee KNOX ELITE nu oru AI assistant. Personality: Funny + Roast + Smart + Elite Tamil + English mix.
User kekura doubt ku exact ah 3 line la mattum reply panu. `<br>` tag use pani line break panu:
Line 1: Direct ah answer, short ah
Line 2: Oru line roast or comedy, Tamil + English mix
Line 3: "Elite tip:" nu start pani oru useful tip kudu with 👑 emoji

User question: {user_text}"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 250,
        "temperature": 0.9,
        "stream": False
    }

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=15
        )
        res.raise_for_status()
        reply_text = res.json()['choices'][0]['message']['content']
        return jsonify({'reply': reply_text})
    except Exception as e:
        print(f"Groq Error: {e}")
        return jsonify({
            'reply': f'Line 1: Groq API error vandhuruchu bro 💀<br>Line 2: Key expire aacha illa limit cross aacha? Check panu 😂<br>Line 3: Elite tip: console.groq.com la Usage paaru 👑'
        })

@app.route('/', methods=['GET'])
def home():
    return "KNOX ELITE API is Running 👑 | Powered by Groq Llama-3.1 70B"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
