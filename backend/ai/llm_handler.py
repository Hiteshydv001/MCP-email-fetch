import google.generativeai as genai
from config.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_response(prompt):
    try:
        response = model.generate_content(prompt)
        logger.debug("Generated response from Gemini LLM")
        print("[DEBUG] Generated response from Gemini LLM")
        return response.text
    except Exception as e:
        logger.error(f"Gemini LLM generation failed: {str(e)}")
        print(f"[ERROR] Gemini LLM generation failed: {str(e)}")
        raise