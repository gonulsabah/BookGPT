from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def create_embedding(query: str) -> np.ndarray:
    """Create a normalized embedding for the given query string."""
    embedding = model.encode(
        [query],
        normalize_embeddings=True
    )
    return embedding.astype("float32")
