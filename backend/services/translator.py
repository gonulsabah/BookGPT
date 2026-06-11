from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from langdetect import detect, DetectorFactory
import torch

DetectorFactory.seed = 0

class FlawlessTranslator:
    def __init__(self):
        # 🚨 HATA VERMEYEN VE SUNUCUDA AKTİF OLAN GÜNCEL MODELLER 🚨
        self.en_tr_path = "Helsinki-NLP/opus-mt-tc-big-en-tr"  # Helsinki'nin güncel ve daha gelişmiş EN->TR modeli
        self.tr_en_path = "Helsinki-NLP/opus-mt-tr-en"         # Zaten çalışan TR->EN modelimiz
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"📦 Kararlı çeviri motoru internetten yükleniyor... (Donanım: {self.device.upper()})")
        
        # Modelleri internetten temizce çekiyoruz (İlk seferde biraz indirecektir)
        self.en_tr_tokenizer = AutoTokenizer.from_pretrained(self.en_tr_path)
        self.en_tr_model = AutoModelForSeq2SeqLM.from_pretrained(self.en_tr_path).to(self.device)
        
        self.tr_en_tokenizer = AutoTokenizer.from_pretrained(self.tr_en_path)
        self.tr_en_model = AutoModelForSeq2SeqLM.from_pretrained(self.tr_en_path).to(self.device)
        
        print("✅ İki motor da sorunsuz ayağa kalktı!")

    def translate(self, text: str) -> str:
        try:
            detected_lang = detect(text)
            
            if detected_lang == "en":
                print(f"🔍 [Dil: İngilizce] -> Türkçeye çevriliyor...")
                inputs = self.en_tr_tokenizer(text, return_tensors="pt", padding=True).to(self.device)
                translated_tokens = self.en_tr_model.generate(**inputs)
                return self.en_tr_tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
            else:
                print(f"🔍 [Dil: Türkçe] -> İngilizceye çevriliyor...")
                inputs = self.tr_en_tokenizer(text, return_tensors="pt", padding=True).to(self.device)
                translated_tokens = self.tr_en_model.generate(**inputs)
                return self.tr_en_tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
                
        except Exception as e:
            print(f"❌ Çeviri Hatası: {e}")
            return text

# --- TEST ---
translator = FlawlessTranslator()

print("\n--- DENEME 1: Türkçe Girdi ---")
print(translator.translate("Sürükleyici bir tarih kitabı öner"))

print("\n--- DENEME 2: İngilizce Girdi ---")
print(translator.translate("Offer a riveting history book on World War Two"))