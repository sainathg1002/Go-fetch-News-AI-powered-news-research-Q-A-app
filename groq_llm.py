import requests

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(prompt, api_key):

    if not api_key:
        return "❌ Groq API key not provided."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        r = requests.post(GROQ_URL, headers=headers, json=payload, timeout=20)
        data = r.json()

        if "choices" not in data:
            return f"⚠️ Groq API Error: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ Request failed: {str(e)}"
