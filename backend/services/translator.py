from transformers import MarianMTModel, MarianTokenizer
import torch

model_name = "Helsinki-NLP/opus-mt-tr-en"

# Model ve tokenizer'ı FastAPI ayağa kalktığında bir kez yükleyecek şekilde ayarlıyoruz
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

def translate_tr_to_en(text: str) -> str:
    try:
        inputs = tokenizer(text, return_tensors="pt", padding=True).to(device)
        translated_tokens = model.generate(**inputs)
        translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translated_text
    except Exception as e:
        print(f"❌ Çeviri Hatası: {e}")
        return text