import faiss
import pandas as pd
from .embedding import create_embedding

# Bunlar main.py içindeki lifespan tarafından doldurulacak, başlangıçta None kalabilir
books = None
index = None


def hybrid_book_recommendation(query: str, translator, top_k: int = 5, alpha: float = 0.7, beta: float = 0.3):
    """
    alpha: semantic similarity ağırlığı
    beta: rating/popularity ağırlığı

    NOT: translator nesnesini artık parametre olarak dışarıdan (main.py - app.state) alıyoruz.
    """

    # Türkçe -> İngilizce (Dışarıdan gelen translator nesnesini kullanıyoruz)
    english_query = translator.translate_tr_to_en(query)

    # Query embedding
    query_vector = create_embedding(english_query)

    # FAISS search
    candidate_count = min(30, len(books))
    distances, indices = index.search(query_vector, candidate_count)

    results = []
    for score, idx in zip(distances[0], indices[0]):
        if idx == -1 or idx >= len(books):
            continue
        row = books.iloc[int(idx)]
        semantic_score = float(score)
        ml_score = float(row["normalized_ml_score"])

        final_score = (alpha * semantic_score + beta * ml_score)

        results.append({
            "title": row["title"],
            "author": row["author"],
            "genres": row["genres"],
            "semantic_score": round(semantic_score, 4),
            "ml_quality_score": round(ml_score, 4),
            "final_score": round(final_score, 4),
            "description": row["description"],
            "avg_rating": row["avg_rating"]
        })

    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values("final_score", ascending=False)

    return result_df.head(top_k)
