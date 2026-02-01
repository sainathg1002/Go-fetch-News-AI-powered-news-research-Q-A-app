import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(prompt):
    if not GROQ_API_KEY:
        return "❌ GROQ_API_KEY not found. Check your .env file."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    try:
        r = requests.post(GROQ_URL, headers=headers, json=payload, timeout=20)
        data = r.json()

        # 🔥 SAFETY CHECK
        if "choices" not in data:
            return f"⚠️ Groq API Error: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ Request failed: {str(e)}"

    print("Groq key loaded:", bool(GROQ_API_KEY))

