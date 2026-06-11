import faiss
import pandas as pd
from fastapi import FastAPI, HTTPException, Request

# Kendi yazdığınız servisleri import ediyoruz
from services import search, translator as translator_module

app = FastAPI(title="BookGPT API")

# Modellerin durumunu global değişkenlerde tutuyoruz
bot_translator = None


def init_resources():
    """Modelleri ve verileri SADECE ilk istek geldiğinde yükler."""
    global bot_translator

    if bot_translator is not None:
        return

    print(
        "⚠️  [LAZY LOADING] İlk istek geldi, modeller şimdi hafızaya yükleniyor..."
    )

    try:
        # 1. Çeviri Modelini Yükle
        print("🤖 1/3: Çeviri modeli yükleniyor...")
        translator_obj = translator_module.BookTranslator()
        translator_obj.load_model()
        bot_translator = translator_obj

        # 2. Verileri Yükle
        print("📚 2/3: Veritabanı (CSV) okunuyor...")
        search.books = pd.read_csv("data/books.csv")

        print("🧠 3/3: FAISS indeksi yükleniyor...")
        search.index = faiss.read_index("data/books.faiss")

        print("✅ [BAŞARILI] Tüm kaynaklar hafızaya alındı!")

    except Exception as e:
        print(f"❌ Kaynaklar yüklenirken hata oluştu: {e}")
        raise RuntimeError("Modeller yüklenemedi!")


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "FastAPI tamamen aktif! Öneri almak için /recommend endpoint'ini kullanın.",
    }


@app.get("/recommend")
def recommend(query: str, top_k: int = 5):
    """İlk çağrıldığında modelleri yükler, sonraki çağrılarda direkt çalışır."""
    global bot_translator

    if bot_translator is None:
        init_resources()

    try:
        # Arama fonksiyonunu çalıştır
        result_df = search.hybrid_book_recommendation(
            query, translator=bot_translator, top_k=top_k
        )
        return result_df.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Öneri üretilirken hata oluştu: {str(e)}"
        )
