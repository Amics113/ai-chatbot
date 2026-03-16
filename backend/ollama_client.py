import google.generativeai as genai
import os

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("AIzaSyB7rjWaKneaVsvkJzqn8N2WIoJ0Iizu0_0")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Model
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_response(prompt: str, context: str = "") -> str:
    """
    Generate response using Gemini API
    """

    full_prompt = f"""
You are an intelligent AI assistant.

BEHAVIOR RULES:
- Use provided context ONLY if it helps answer the question.
- Ignore irrelevant context.
- Be accurate and logical.
- Keep answers clear and natural.
- Continue conversation smoothly.

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
        return "⚠️ AI model is temporarily unavailable."