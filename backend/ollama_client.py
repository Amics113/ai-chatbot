import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama3-8b-8192"

def generate_response(prompt: str, context: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    }

    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )

    return res.json()["choices"][0]["message"]["content"]
