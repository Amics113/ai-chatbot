import os
import pickle
import faiss
import numpy as np
from backend.rag.embeddings import embed_text


# Get project root directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DOC_DIR = os.path.join(BASE_DIR, "data", "documents")
DB_DIR = os.path.join(BASE_DIR, "data", "vector_db")
DB_PATH = os.path.join(DB_DIR, "index.pkl")

print("📁 Looking for documents in:", DOC_DIR)

if not os.path.exists(DOC_DIR):
    raise FileNotFoundError(f"Folder not found: {DOC_DIR}")

os.makedirs(DB_DIR, exist_ok=True)

texts = []

for file in os.listdir(DOC_DIR):
    if file.endswith(".txt"):
        with open(os.path.join(DOC_DIR, file), "r", encoding="utf-8") as f:
            texts.append(f.read())

if not texts:
    raise ValueError("❌ No .txt files found in data/documents")

# ✅ THIS IS THE CRITICAL FIX
vectors = np.array(
    [embed_text(t) for t in texts],
    dtype=np.float32
)

print("🔢 Vector shape:", vectors.shape)

dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

with open(DB_PATH, "wb") as f:
    pickle.dump((index, texts), f)

print("✅ RAG indexing completed successfully")
