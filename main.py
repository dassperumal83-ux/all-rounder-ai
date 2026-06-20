from flask import Flask, request,jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Gemini API Key ah Render la irundhu edukuradhu
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

@app.route('/')
def home():
    return "Hello from Knox AI! Bot is Live 🚀"

@app.route('/chat')
def chat():
    if model:
        response = model.generate_content("Say hi, I am Knox AI")
        return response.text
    else:
        return "API Key not set yet bro!"
        
if__name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)

