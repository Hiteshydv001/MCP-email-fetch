from utils.logger import get_logger

logger = get_logger(__name__)

def clean_text(text):
    try:
        cleaned = text.strip().replace('\n', ' ').replace('\r', '')
        logger.debug("Text cleaned successfully")
        print("[DEBUG] Text cleaned successfully")
        return cleaned
    except Exception as e:
        logger.error(f"Text cleaning failed: {str(e)}")
        print(f"[ERROR] Text cleaning failed: {str(e)}")
        raise