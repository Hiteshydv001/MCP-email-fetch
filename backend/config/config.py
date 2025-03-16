# Replace config/config.py with this
import os
from dotenv import load_dotenv

# Explicitly specify UTF-8 encoding and handle BOM
load_dotenv(encoding='utf-8-sig')  # 'utf-8-sig' skips BOM (Byte Order Mark)

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/email_assistant")
    GMAIL_API_SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    DEBUG = os.getenv("DEBUG", "True") == "True"
    LOG_LEVEL = "DEBUG" if DEBUG else "INFO"