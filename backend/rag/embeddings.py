import os
import numpy as np
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def embed_text(text: str):
    result = genai.embed_content(
        model="models/embedding-001",
        content=text
    )

    vector = np.array(result["embedding"]).astype("float32")
    return vector.reshape(1, -1)