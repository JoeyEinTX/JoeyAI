import os
class Config:
    PORT = int(os.getenv("PORT", 5000))
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "deepseek-r1:7b")
    AUTO_SAVE_CHATS = os.getenv("AUTO_SAVE_CHATS", "true").lower() == "true"
