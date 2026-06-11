import numpy as np
import pandas as pd
import faiss

from services.embedding import create_embedding
# from services.translator import translate_query


# Load once
books = pd.read_csv("data/books.csv")
index = faiss.read_index("data/books.faiss")


def hybrid_book_recommendation(query, top_k=5, alpha=0.7, beta=0.3):
    """
    alpha:
        semantic similarity ağırlığı

    beta:
        rating/popularity ağırlığı
    """

    # ürkçe -> İngilizce
    # english_query = translate_query(query)
    english_query = query
    # Query embedding
    query_vector = create_embedding(english_query)

    # 3) FAISS search
    candidate_count = min(30, len(books))

    distances, indices = index.search(query_vector, candidate_count)

    results = []

    for score, idx in zip(distances[0], indices[0]):
        row = books.iloc[idx]
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

    result_df = result_df.sort_values(
        "final_score",
        ascending=False
    )

    return result_df.head(top_k)
