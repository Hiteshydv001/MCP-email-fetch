from ai.llm_handler import generate_response
from utils.logger import get_logger

logger = get_logger(__name__)

def rank_email(email_content):
    try:
        prompt = f"Determine the urgency of this email (high, medium, low):\n{email_content}"
        urgency = generate_response(prompt).strip()
        logger.debug(f"Email urgency ranked: {urgency}")
        print(f"[DEBUG] Email urgency ranked: {urgency}")
        return urgency
    except Exception as e:
        logger.error(f"Email ranking failed: {str(e)}")
        print(f"[ERROR] Email ranking failed: {str(e)}")
        raise