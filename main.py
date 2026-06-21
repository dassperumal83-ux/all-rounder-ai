from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
HTML = """

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Knox - Intelligence, Elevated</title>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
        background: #0A0A0A;
        color: #E5E5E5;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        height: 100vh;
        overflow: hidden;
        position: relative;
    }

    canvas {
        position: fixed;
        top: 0;
        left: 0;
        z-index: 0;
    }

   .container {
        position: relative;
        z-index: 1;
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        padding: 40px 20px;
    }

   .brand {
        text-align: center;
        margin-top: 60px;
    }

   .brand h1 {
        font-size: 48px;
        font-weight: 700;
        letter-spacing: 4px;
        background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }

   .brand p {
        font-size: 14px;
        color: #888;
        letter-spacing: 2px;
        font-weight: 300;
    }

   .chat-area {
        width: 100%;
        max-width: 800px;
        flex: 1;
        overflow-y: auto;
        padding: 20px 0;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

   .chat-area::-webkit-scrollbar {
        width: 4px;
    }

   .chat-area::-webkit-scrollbar-thumb {
        background: #D4AF37;
        border-radius: 2px;
    }

   .msg {
        max-width: 70%;
        padding: 16px 20px;
        border-radius: 12px;
        line-height: 1.6;
        font-size: 15px;
        animation: fadeIn 0.3s ease;
    }

   .user-msg {
        align-self: flex-end;
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid rgba(212, 175, 55, 0.3);
    }

   .knox-msg {
        align-self: flex-start;
        background: #1A1A1A;
        border-left: 3px solid #D4AF37;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

   .input-wrapper {
        width: 100%;
        max-width: 700px;
        position: relative;
        margin-bottom: 40px;
    }

   .mic-btn {
        position: absolute;
        left: 12px;
        top: 50%;
        transform: translateY(-50%);
        background: transparent;
        border: none;
        color: #D4AF37;
        font-size: 22px;
        cursor: pointer;
        padding: 8px;
        transition: all 0.3s ease;
        z-index: 2;
    }

   .mic-btn.listening {
        color: #FF4444;
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: translateY(-50%) scale(1); }
        50% { transform: translateY(-50%) scale(1.3); }
    }

   .input-box {
        width: 100%;
        background: #0F0F0F;
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 16px;
        padding: 20px 60px 20px 60px;
        color: #E5E5E5;
        font-size: 16px;
        font-family: inherit;
        outline: none;
        transition: all 0.3s ease;
    }

   .input-box:focus {
        border-color: #D4AF37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }

   .input-box::placeholder {
        color: #555;
        letter-spacing: 1px;
    }

   .send-btn {
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        background: transparent;
        border: none;
        color: #D4AF37;
        font-size: 24px;
        cursor: pointer;
        padding: 8px;
        transition: all 0.3s ease;
        z-index: 2;
    }

   .send-btn:hover {
        transform: translateY(-50%) scale(1.2);
        text-shadow: 0 0 10px #D4AF37;
    }

   .footer {
        position: absolute;
        bottom: 12px;
        right: 20px;
        font-size: 10px;
        color: #444;
    }

    @media (max-width: 768px) {
       .brand h1 { font-size: 36px; }
       .msg { max-width: 85%; font-size: 14px; }
       .input-wrapper { max-width: 100%; }
       .brand { margin-top: 40px; }
    }
</style>
</head>
<body>
<canvas id="particles"></canvas>

<div class="container">
    <div class="brand">
        <h1>KNOX</h1>
        <p>Intelligence, Elevated</p>
    </div>

    <div class="chat-area" id="chatArea">
        <div class="msg knox-msg">
            Welcome, CEO. Command me.
        </div>
    </div>

    <div class="input-wrapper">
        <button class="mic-btn" id="micBtn" onclick="toggleVoice()">🎤</button>
        <input type="text" class="input-box" id="inputBox" placeholder="Command..." autocomplete="off">
        <button class="send-btn" onclick="sendMsg()">→</button>
    </div>

    <div class="footer">Knox v1.0</div>
</div>

<script>
// Gold particles background
const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];
for(let i = 0; i < 50; i++) {
    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2 + 0.5,
        speedX: Math.random() * 0.4 - 0.2,
        speedY: Math.random() * 0.4 - 0.2
    });
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'rgba(212, 175, 55, 0.4)';
    particles.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        p.x += p.speedX;
        p.y += p.speedY;
        if(p.x < 0 || p.x > canvas.width) p.speedX *= -1;
        if(p.y < 0 || p.y > canvas.height) p.speedY *= -1;
    });
    requestAnimationFrame(animate);
}
animate();

// Chat logic
const inputBox = document.getElementById('inputBox');
const chatArea = document.getElementById('chatArea');

function addMsg(text, isUser) {
    const div = document.createElement('div');
    div.className = 'msg ' + (isUser? 'user-msg' : 'knox-msg');
    div.textContent = text;
    chatArea.appendChild(div);
    chatArea.scrollTop = chatArea.scrollHeight;
}

async function sendMsg() {
    const text = inputBox.value.trim();
    if(!text) return;

    addMsg(text, true);
    inputBox.value = '';

    const typing = document.createElement('div');
    typing.className = 'msg knox-msg';
    typing.textContent = 'Knox is thinking...';
    chatArea.appendChild(typing);

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({msg: text})
        });
        const data = await res.json();
        typing.remove();
        addMsg(data.reply, false);
    } catch(e) {
        typing.remove();
        addMsg('Error: Knox offline. Check server.', false);
    }
}

inputBox.addEventListener('keypress', e => {
    if(e.key === 'Enter') sendMsg();
});

// Voice Recognition
let recognition = null;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';

    recognition.onresult = (e) => {
        inputBox.value = e.results[0][0].transcript;
        document.getElementById('micBtn').classList.remove('listening');
    };

    recognition.onerror = () => {
        document.getElementById('micBtn').classList.remove('listening');
    };

    recognition.onend = () => {
        document.getElementById('micBtn').classList.remove('listening');
    };
}

function toggleVoice() {
    const micBtn = document.getElementById('micBtn');
    if (!recognition) {
        alert('Voice not supported in this browser. Use Chrome for best experience.');
        return;
    }

    if (micBtn.classList.contains('listening')) {
        recognition.stop();
        micBtn.classList.remove('listening');
    } else {
        recognition.start();
        micBtn.classList.add('listening');
    }
}

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get('msg', '')
    
    if msg.lower() == 'hi':
        reply = "Hello CEO. Knox is online and ready. Command me."
    elif msg.lower() == 'test':
        reply = "Voice + UI + Backend all working perfectly, sir."
    else:
        reply = f"Received: {msg}. Knox is ready for your next command."
    
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
