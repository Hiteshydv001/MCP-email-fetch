from ai.llm_handler import generate_response
from utils.logger import get_logger

logger = get_logger(__name__)

def analyze_sentiment(email_content):
    try:
        prompt = f"Classify the sentiment of this email as positive, negative, or neutral:\n{email_content}"
        sentiment = generate_response(prompt).strip()
        logger.debug(f"Sentiment analyzed: {sentiment}")
        print(f"[DEBUG] Sentiment analyzed: {sentiment}")
        return sentiment
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        print(f"[ERROR] Sentiment analysis failed: {str(e)}")
        return "N/A"