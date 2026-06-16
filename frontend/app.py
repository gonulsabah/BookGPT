import streamlit as st
import requests
from datetime import datetime


st.set_page_config(
    page_title="BookGPT | Akıllı Kitap Öneri Sistemi",
    page_icon="📚",
    layout="wide"
)

# Arama kutusunun değerini session_state üzerinden yönetiyoruz
if "search_query_val" not in st.session_state:
    st.session_state.search_query_val = ""

# ==========================================
# SIDEBAR (KULLANICI PANELİ) TASARIMI
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #E5A93C;'>📊 Kullanıcı Paneli</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h4 style='color: #F5F0EA;'>🔍 Arama Metrikleri</h4>", unsafe_allow_html=True)
    top_k = st.slider("Önerilecek Kitap Sayısı", min_value=1, max_value=10, value=5)
    
    st.markdown("---")
    st.markdown("<h4 style='color: #F5F0EA;'>🧠 Hibrit Arama Ağırlığı</h4>", unsafe_allow_html=True)
    st.caption("Anlamsal ve Kelime Bazlı Arama Dengesi:")
    alpha = st.slider("Ağırlık Katsayısı", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    
    
    st.markdown("---")
    st.markdown("<h4 style='color: #F5F0EA;'>📅 Kitap Dönemi Filtresi</h4>", unsafe_allow_html=True)
    current_year = datetime.now().year
    year_range = st.slider("Yayın Yılı Aralığı", min_value=1800, max_value=current_year, value=(1950, current_year))
    
    st.markdown("---")
    st.markdown("<h4 style='color: #E5A93C;'>🛠️ Teknolojik Altyapı</h4>", unsafe_allow_html=True)
    st.markdown("""
    * **Backend:** FastAPI
    * **Vektör Veritabanı:** FAISS
    * **Çeviri Motoru:** Google Translator
    * **Dil Tespiti:** Google LangDetect
    * **Arama Algoritması:** Hybrid Search
    """)

# ==========================================
# ANA SAYFA TASARIMI
# ==========================================
st.markdown("<h1 style='text-align: center; color: #E5A93C;'>📚 BookGPT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #B5A89C; font-style: italic; font-size: 18px;'>Hibrit Kitap Öneri Asistanı</p>", unsafe_allow_html=True)
st.markdown("---")

# Kartlar Bölümü
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.markdown("""
    <div style="background-color: #322E2A; padding: 18px; border-radius: 8px; border-top: 4px solid #E5A93C; min-height: 150px;">
        <h5 style="color: #E5A93C; margin: 0 0 10px 0; font-size: 20px; font-weight: bold;">🌐 Çok Dilli Destek</h5>
        <p style="color: #F5F0EA; font-size: 15px; line-height: 1.6; margin: 0;">İstediğiniz dilde, sistem dili otomatik tespit eder ve global kütüphanede arama yapar.</p>
    </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown("""
    <div style="background-color: #322E2A; padding: 18px; border-radius: 8px; border-top: 4px solid #E5A93C; min-height: 150px;">
        <h5 style="color: #E5A93C; margin: 0 0 10px 0; font-size: 20px; font-weight: bold;">🎛️ Hibrit Skorlama</h5>
        <p style="color: #F5F0EA; font-size: 15px; line-height: 1.6; margin: 0;">Puanlama ile anlamsal yakınlık harmanlanarak en doğru eşleşme üretilir.</p>
    </div>
    """, unsafe_allow_html=True)

with col_info3:
    st.markdown("""
    <div style="background-color: #322E2A; padding: 18px; border-radius: 8px; border-top: 4px solid #E5A93C; min-height: 150px;">
        <div style="margin-bottom: 12px;">
            <span style="font-size: 38px; display: inline-block; vertical-align: middle; line-height: 1; margin-right: 8px;">🤖</span>
            <span style="color: #E5A93C; font-size: 20px; font-weight: bold; display: inline-block; vertical-align: middle; padding-top: 4px;">Yapay Zeka Desteği</span>
        </div>
        <p style="color: #F5F0EA; font-size: 15px; line-height: 1.6; margin: 0;">LLM ile yapılan kitap önerileri desteklenir.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

# ==========================================
# ARAMA VE ÖNERİ BÖLÜMÜ
# ==========================================
st.markdown("<h4 style='color: #E5A93C; margin-bottom: -15px; font-size: 22px;'>🧐 Nasıl bir kitap okumak istersiniz?</h4>", unsafe_allow_html=True)

# Girdi alanını session_state değerine bağlıyoruz
user_query = st.text_input(
    "", 
    value=st.session_state.search_query_val,
    placeholder="Örn: Sürpriz sonlu, felsefi ögeler barındıran akıcı bir distopya romanı...",
    key="recommend_query"
)

col_space1, col_btn_recommend, col_space2 = st.columns([2, 4, 2])

with col_btn_recommend:
    submit_button = st.button("✨ Bana Kitap Öner", use_container_width=True)

# Öneri İstek Mantığı
# ==========================================
# ÖNERİ İSTEK MANTIĞI (GÜNCELLENMİŞ)
# ==========================================
if submit_button:
    # Kullanıcı kutuda manuel değişiklik yaptıysa state güncel kalsın
    st.session_state.search_query_val = user_query 
    
    if user_query:
        try:
            with st.spinner("🤖 BookGPT derinlemesine arama yapıyor..."):
                # Backend'e normal kullanıcı sorgusunu ve slider parametrelerini gönderiyoruz
                response = requests.get(
                    "http://127.0.0.1:8000/recommend", 
                    params={
                        "query": user_query,
                        "top_k": top_k,
                        "alpha": alpha,
                        "beta": 1.0 - alpha
                    },
                    timeout=60
                )
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Backend'den (main.py) dönen iki ana yapıyı ayıklıyoruz
                english_query = response_data.get("search_query_english", "")
                data = response_data.get("results", [])
                
                # ========================================================
                # İSTEDİĞİNİZ ÖZELLİK: FAISS Vektör Arama Analiz Kutusu
                # ========================================================
                st.markdown(f"""
                <div style="background-color: #1E232A; padding: 16px; border-radius: 8px; margin-bottom: 25px; border-left: 5px solid #4A90E2; box-shadow: 0px 2px 10px rgba(0,0,0,0.15);">
                    <span style="color: #4A90E2; font-weight: bold; font-size: 16px;">🧠 Metin Analizi:</span><br>
                    <span style="color: #B5A89C; font-size: 14px;">Girdiğiniz Metin:</span> <span style="color: #F5F0EA; font-style: italic;">"{user_query}"</span><br>
                    <span style="color: #4A90E2; font-weight: bold; font-size: 18px;">➡️</span> 
                    <span style="color: #B5A89C; font-size: 14px;">Aranan Metin:</span> <span style="color: #E5A93C; font-weight: bold; font-size: 15px;">"{english_query}"</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Sonuçların listelenmesi
                st.markdown(f"<h3 style='color: #E5A93C;'>🎯 Sizin İçin Seçtiğimiz En İyi {len(data)} Kitap:</h3>", unsafe_allow_html=True)
                
                if isinstance(data, list) and len(data) > 0:
                    for idx, book in enumerate(data, 1):
                        title = book.get("title", "Bilinmeyen Kitap")
                        author = book.get("author", "Bilinmeyen Yazar")
                        genres = book.get("genres", "Belirtilmemiş")
                        description = book.get("description", "Açıklama bulunmuyor.")
                        
                        # Arama detay skorlarını da görmek istersen diye ekledim (isteğe bağlı tutabilirsin)
                        final_score = book.get("final_score", 0)
                        
                        st.markdown(f"""
                        <div style="background-color: #3A3530; padding: 22px; border-radius: 12px; border-left: 6px solid #E5A93C; margin-bottom: 18px; box-shadow: 0px 4px 15px rgba(0,0,0,0.2);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h4 style="margin: 0; color: #FFFFFF; font-size: 19px; font-weight: 700;">{idx}. {title}</h4>
                                <span style="background-color: #E5A93C; color: #3A3530; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;">Skor: {final_score}</span>
                            </div>
                            <p style="margin: 6px 0; color: #E5A93C; font-weight: bold; font-size: 14px;">✍️ Yazar: {author} | 🏷️ Tür: {genres}</p>
                            <hr style="border: 0; border-top: 1px solid #4E4741; margin: 12px 0;">
                            <p style="margin: 5px 0 0 0; color: #E1D9D1; font-size: 15px; line-height: 1.6;">{description}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Kriterlerinize uygun bir kitap bulunamadı.")
            else:
                st.error(f"Backend Hatası: {response.status_code}")
        except Exception as e:
            st.error(f"💥 Bağlantı Hatası: {e}")
    else:
        st.warning("Lütfen önce aramak istediğiniz kitap tarzını yazın!")