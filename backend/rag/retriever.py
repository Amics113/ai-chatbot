import os
import pickle
import faiss
import numpy as np
from backend.rag.embeddings import embed_text

VECTOR_DB = "data/vector_db/index.faiss"
TEXT_DB = "data/vector_db/texts.pkl"

SIMILARITY_THRESHOLD = 0.6  # Ignore weak matches


def retrieve_context(query: str, k: int = 3) -> str:
    # If database does not exist
    if not os.path.exists(VECTOR_DB) or not os.path.exists(TEXT_DB):
        return ""

    # Load FAISS index
    index = faiss.read_index(VECTOR_DB)

    # Load stored texts
    with open(TEXT_DB, "rb") as f:
        texts = pickle.load(f)

    # Generate embedding
    query_vector = embed_text(query)

    # Convert to numpy if needed
    query_vector = np.array(query_vector).astype("float32")

    # Search FAISS
    D, I = index.search(query_vector, k)

    # If similarity too low → ignore RAG
    if len(D) == 0 or D[0][0] < SIMILARITY_THRESHOLD:
        return ""

    # Retrieve matching texts
    results = []
    for idx in I[0]:
        if idx < len(texts):
            results.append(texts[idx])

    return "\n".join(results)