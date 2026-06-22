# 📚 BookGPT — Hybrid AI Book Recommendation System

BookGPT is an AI-powered book recommendation system that combines semantic search, machine learning ranking, and LLM-based explanations to provide personalized book recommendations.

The system detects the user's query language, translates non-English queries into English for semantic retrieval, ranks books using a hybrid scoring strategy, and generates LLM-powered explanations.

---

## Features

- 🔎 Semantic book search using Sentence Transformers
- ⚡ Fast vector similarity retrieval with FAISS
- 📊 ML-based book quality scoring
- 🔀 Hybrid recommendation ranking
- 🤖 LLM-powered recommendation explanations
- 💾 LLM response caching to reduce API usage
- 🐳 Dockerized backend and frontend
- ☁️ Deployed on Google Cloud Run

---

## Architecture
            Goodreads Dataset
                    |
                    v
          Exploratory Data Analysis
                    |
                    v
          Feature Engineering
          - avg_rating
          - num_ratings
          - metadata
                    |
                    v
          ML Quality Score
                    |
                    |
                    v

        Sentence Transformer Model
                    |
                    v
          Book Embeddings
                    |
                    v
             FAISS Index
          (books.faiss)

            User Query
                |
                v
        Sentence Detect/Query Embedding
                |
                v
        FAISS Similarity Search
                |
        +---------------------+
                |
                v
        Semantic Score Book Metadata
            ML Score
                |
                v

            Hybrid Ranking
                |
                v
            Top-K Books
                |
                v
        LLM Explain Layer
                |
                v
        Personalized Explanation

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- Pandas
- Scikit-learn
- Sentence Transformers
- FAISS
- LangChain
- Gemini API


### Frontend

- Streamlit


### Infrastructure

- Docker
- Docker Compose
- Google Cloud Run
- Artifact Registry


---

## 📂 Project Structure
![alt text](<Screenshot 2026-06-22 at 10.49.52.png>)
![alt text](<Screenshot 2026-06-22 at 10.49.34.png>)