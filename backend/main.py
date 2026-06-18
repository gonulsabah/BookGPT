import os
import faiss
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sympy import im
from langchain.chat_models import init_chat_model

# Kendi yazdığınız servisleri import ediyoruz
from backend.services import search, translator as translator_module, \
    llm as llm_module

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data")

app = FastAPI(title="BookGPT API")

bot_translator = None
llm = None
gemini_api_key = os.getenv("GEMINI_API_KEY")


class LanguageDetectionRequest(BaseModel):
    text: str


def init_resources():
    """Modelleri ve verileri SADECE ilk istek geldiğinde yükler."""

    global bot_translator

    if bot_translator is not None:
        return

    print(
        "[LAZY LOADING] İlk istek geldi, modeller şimdi hafızaya yükleniyor..."
    )

    try:
        # 1. Çeviri Modelini Yükle
        print("[1/3] Çeviri modeli yükleniyor...")
        translator_obj = translator_module.FlawlessTranslator()
        translator_obj.load_model()
        bot_translator = translator_obj

        # 2. Verileri Yükle
        print("[2/3] Veritabanı (CSV) okunuyor...")
        search.books = pd.read_csv(
            os.path.join(DATA_PATH, "prepared_books.csv"))

        print("[3/3] FAISS indeksi yükleniyor...")
        search.index = faiss.read_index(
            os.path.join(DATA_PATH, "books.faiss"))

        print("[BAŞARILI] Tüm kaynaklar hafızaya alındı!")

        global llm

        llm = init_chat_model(
            "gemini-2.5-flash-lite",
            model_provider="google_genai",
            api_key=gemini_api_key,
            temperature=0.2
        )

    except Exception as e:
        print(f"Kaynaklar yüklenirken hata oluştu: {e}")
        raise RuntimeError("Modeller yüklenemedi!")


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "FastAPI tamamen aktif! Öneri almak için /recommend endpoint'ini kullanın.",
    }


@app.get("/recommend")
def recommend(query: str, top_k: int = 5, alpha: float = 0.7, beta: float = 0.3):
    global bot_translator

    # Modeller yüklenmediyse ilk istekte yükle
    if bot_translator is None:
        init_resources()

    try:

        # 2. ADIM: FAISS hibrit aramasına İngilizceye çevrilmiş sorguyu gönder
        result_df, english_query = search.hybrid_book_recommendation(
            query=query, translator=bot_translator, top_k=top_k, alpha=alpha, beta=beta)

        llm_response = llm_module.recommend_with_explanation(
            query=query, books=result_df, llm=llm)
        return {
            "search_query_english": english_query,
            "results": result_df.to_dict(orient="records"),
            "explanation": llm_response
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Öneri üretilirken hata oluştu: {str(e)}"
        )


@app.post("/detect-language")
def detect_language(request: LanguageDetectionRequest):
    global bot_translator

    if bot_translator is None:
        init_resources()

    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Metin boş olamaz.")

    try:
        lang = bot_translator.detect_language(request.text)
        return {
            "text": request.text,
            "detected_language": lang,
            "status": "success" if lang != "unknown" else "failed"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Dil tespiti sırasında hata oluştu: {str(e)}"
        )
