import torch
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


class FlawlessTranslator:

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        print(
            "[BAŞARILI] Çeviri motoru bulut üzerinden saniyeler içinde aktif edildi!"
        )
    def detect_language(self, text: str) -> str:
        """
        Girilen metnin hangi dilde olduğunu tespit eder.
        """
        try:
            if not text or not text.strip():
                return "unknown"
            
            detected_lang = detect(text)
            print(f"[Dil Tespiti]: {detected_lang}")
            return detected_lang
        except Exception as e:
            print(f"Dil tespiti sırasında hata: {e}")
            return "unknown"
    def translate(self, text: str) -> str:
        try:
            detected_lang = self.detect_language(text)

            if detected_lang == "en":
                print(f"[Dil: İngilizce]")
                return text
            else:

                source_lang = detected_lang.upper()
                target_lang = "EN"

                print(f"🔄 [Dil: {source_lang}] -> İngilizceye çevriliyor...")
                translated = GoogleTranslator(source=detected_lang, target="en").translate(text)

                print(f"✨ [{source_lang} -> {target_lang}] Sonuç: {translated}")
                return translated
        except Exception as e:
            print(f"Çeviri Hatası: {e}")
            return text

    def translate_tr_to_en(self, text: str) -> str:
        return self.translate(text)
