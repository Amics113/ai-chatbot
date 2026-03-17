import google.generativeai as genai
import os

# read API key from Render environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# configure Gemini only if key exists
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_response(prompt: str, context: str = "") -> str:

    if not GEMINI_API_KEY:
        return "⚠️ Gemini API key not configured."

    full_prompt = f"""
You are an intelligent AI assistant.

Conversation Memory:
{context}

User Question:
{prompt}

Assistant Response:
""".strip()

    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()

    except Exception as e:
        print("Gemini error:", e)
        return "⚠️ AI model temporarily unavailable."