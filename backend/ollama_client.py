import requests

# 🔁 Replace with your NGROK URL (updates when ngrok restarts)
OLLAMA_URL = "https://YOUR_OLLAMA_NGROK_URL/api/generate"

MODEL_NAME = "my-llama-lora"  # ✅ IMPORTANT: your LoRA model name

def generate_response(prompt: str, context: str = "") -> str:
    full_prompt = f"""
You are an AI assistant.

Context:
{context}

User:
{prompt}

Assistant:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False
    }

    res = requests.post(OLLAMA_URL, json=payload, timeout=300)

    if res.status_code != 200:
        return "❌ Ollama error"

    return res.json().get("response", "").strip()
