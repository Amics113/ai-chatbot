import os
import pickle
import faiss
from backend.rag.embeddings import embed_text

VECTOR_DB = "data/vector_db/index.faiss"
TEXT_DB = "data/vector_db/texts.pkl"

SIMILARITY_THRESHOLD = 0.6   # ⭐ key improvement

def retrieve_context(query: str, k: int = 3) -> str:
    if not os.path.exists(VECTOR_DB):
        return ""

    index = faiss.read_index(VECTOR_DB)

    with open(TEXT_DB, "rb") as f:
        texts = pickle.load(f)

    query_vector = embed_text(query)
    D, I = index.search(query_vector, k)

    # If similarity too low → ignore RAG
    if D[0][0] < SIMILARITY_THRESHOLD:
        return ""

    results = [texts[i] for i in I[0] if i < len(texts)]
    return "\n".join(results)
