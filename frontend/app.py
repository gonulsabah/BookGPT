import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="BookGPT | Akıllı Kitap Öneri Sistemi",
    page_icon="📚",
    layout="wide"  # Sayfayı genişleterek yan paneli daha efektif kullanıyoruz
)

# ==========================================
# SIDEBAR (KULLANICI PANELİ) TASARIMI
# ==========================================
with st.sidebar:
    # 3. İkon değişti: ⚙️ yerine 📊 geldi
    st.markdown("<h2 style='color: #E5A93C;'>📊 Kullanıcı Paneli</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Parametre Ayarları
    st.markdown("<h4 style='color: #F5F0EA;'>🔍 Arama Metrikleri</h4>", unsafe_allow_html=True)
    top_k = st.slider("Önerilecek Kitap Sayısı", min_value=1, max_value=10, value=5)
    
    st.markdown("---")
    st.markdown("<h4 style='color: #F5F0EA;'>🧠 Hibrit Arama Ağırlığı</h4>", unsafe_allow_html=True)
    st.caption("Dense (Anlamsal) ve Sparse (Kelime bazlı) arama dengesi:")
    alpha = st.slider("Ağırlık Katsayısı (Alpha)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    
    # 4. Semantik Skorlama Alanı Eklendi
    st.markdown("---")
    st.markdown("<h4 style='color: #F5F0EA;'>✨ Gelişmiş Ayarlar</h4>", unsafe_allow_html=True)
    semantic_weight = st.slider("Semantik (Anlamsal) Hassasiyet", min_value=0.0, max_value=1.0, value=0.8, step=0.1)
    
    # 5. Publish Date (Yayın Yılı) Filtresi Eklendi
    st.markdown("---")
    st.markdown("<h4 style='color: #F5F0EA;'>📅 Kitap Dönemi Filtresi</h4>", unsafe_allow_html=True)
    current_year = datetime.now().year
    # Kullanıcı çift taraflı kaydırarak yıl aralığı seçebilir (Örn: 1950 - 2026)
    year_range = st.slider("Yayın Yılı Aralığı", min_value=1800, max_value=current_year, value=(1950, current_year))
    
    st.markdown("---")
    # Proje Künyesi ve Teknolojiler
    st.markdown("<h4 style='color: #E5A93C;'>🛠️ Teknolojik Altyapı</h4>", unsafe_allow_html=True)
    st.markdown("""
    * **Backend:** FastAPI
    * **Vektör Veritabanı:** FAISS
    * **Çeviri Motoru:** Deep Learning Model
    * **Dil Tespiti:** Google LangDetect
    * **Arama Algoritması:** Hybrid Search
    """)

# ==========================================
# ANA SAYFA TASARIMI
# ==========================================

# Başlık Bölümü
st.markdown("<h1 style='text-align: center; color: #E5A93C;'>📚 BookGPT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #B5A89C; font-style: italic; font-size: 18px;'>Hibrit Kitap Öneri Asistanı</p>", unsafe_allow_html=True)
st.markdown("---")

# Sayfa Boş Kalmasın Diye: "Nasıl Çalışır?" Kartları (3 Sütun)
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.markdown("""
    <div style="background-color: #322E2A; padding: 18px; border-radius: 8px; border-top: 4px solid #E5A93C; min-height: 150px;">
        <h5 style="color: #E5A93C; margin: 0 0 10px 0; font-size: 20px; font-weight: bold;">🌐 Çok Dilli Destek</h5>
        <p style="color: #F5F0EA; font-size: 15px; line-height: 1.6; margin: 0;">İstediğiniz dilde arama yapabilirsiniz. Sistem dili otomatik tespit eder ve global kütüphanede arama yapar.</p>
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

# margin-bottom: -15px; yaparak aşağıdaki input kutusunu kendine doğru yukarı çektik!
st.markdown("<h4 style='color: #E5A93C; margin-bottom: -15px; font-size: 22px;'>🧐 Nasıl bir kitap okumak istersiniz?</h4>", unsafe_allow_html=True)

user_query = st.text_input(
    "", 
    placeholder="Örn: Sürpriz sonlu, felsefi ögeler barındıran akıcı bir distopya romanı..."
)

# Buton
col_btn1, col_btn2, col_btn3 = st.columns([1, 1.5, 1])
with col_btn2:
    submit_button = st.button("✨ Bana Kitap Öner", use_container_width=True)

# Sonuç Ekranı
if submit_button:
    if user_query:
        try:
            with st.spinner("🤖 BookGPT derinlemesine arama yapıyor ve dili analiz ediyor..."):
                # Yeni eklenen parametreleri (semantic_weight, min_year, max_year) url parametrelerine ekliyoruz
                response = requests.get(
                    "http://127.0.0.1:8000/recommend", 
                    params={
                        "query": user_query,
                        "top_k": top_k,
                        "alpha": alpha,
                        "beta": 1.0 - alpha,
                        "semantic_weight": semantic_weight,          # Yeni eklenen semantik ağırlık
                        "min_year": year_range[0],                    # Seçilen başlangıç yılı
                        "max_year": year_range[1]                     # Seçilen bitiş yılı
                    },
                    timeout=60
                )
            
            if response.status_code == 200:
                data = response.json()
                st.markdown(f"<h3 style='color: #E5A93C;'>🎯 Sizin İçin Seçtiğimiz En İyi {len(data)} Kitap:</h3>", unsafe_allow_html=True)
                
                if isinstance(data, list) and len(data) > 0:
                    for idx, book in enumerate(data, 1):
                        title = book.get("title", book.get("book_name", "Bilinmeyen Kitap"))
                        author = book.get("author", book.get("authors", "Bilinmeyen Yazar"))
                        description = book.get("description", book.get("summary", "Açıklama bulunmuyor."))
                        
                        st.markdown(f"""
                        <div style="
                            background-color: #3A3530; 
                            padding: 22px; 
                            border-radius: 12px; 
                            border-left: 6px solid #E5A93C; 
                            margin-bottom: 18px;
                            box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
                        ">
                            <h4 style="margin: 0; color: #FFFFFF; font-size: 19px; font-weight: 700;">{idx}. {title}</h4>
                            <p style="margin: 6px 0; color: #E5A93C; font-weight: bold; font-size: 14px;">✍️ Yazar: {author}</p>
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