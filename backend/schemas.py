from pydantic import BaseModel

class LanguageDetectionRequest(BaseModel):
    text: str

class LanguageDetectionResponse(BaseModel):
    detected_language: str
    status: str