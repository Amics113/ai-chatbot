import subprocess

MODEL_NAME = "llama3:8b"   # 🔁 make sure this matches `ollama list`

def generate_response(prompt: str, context: str = "") -> str:
    full_prompt = f"""
You are a helpful AI assistant.

Context:
{context}

User:
{prompt}

Answer clearly:
""".strip()

    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME],
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=120
        )

        output = result.stdout.strip()

        if not output:
            return "⚠️ Model returned empty response"

        return output

    except Exception as e:
        return f"⚠️ Ollama error: {str(e)}"
