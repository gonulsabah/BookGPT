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

    def translate(self, text: str) -> str:
        try:
            detected_lang = detect(text)

            if detected_lang == "en":
                print(f"[Dil: İngilizce] -> Türkçeye çevriliyor...")
                translated = GoogleTranslator(source="en", target="tr").translate(
                    text
                )
                print(f"Çeviri Sonucu (EN->TR): {translated}")
                return translated
            else:
                print(f"[Dil: Türkçe] -> İngilizceye çevriliyor...")
                translated = GoogleTranslator(source="tr", target="en").translate(
                    text
                )
                print(f"Çeviri Sonucu (TR->EN): {translated}")
                return translated

        except Exception as e:
            print(f"Çeviri Hatası: {e}")
            return text

    def translate_tr_to_en(self, text: str) -> str:
        return self.translate(text)
