from ai.llm_handler import generate_response
from utils.logger import get_logger

logger = get_logger(__name__)

def summarize_thread(thread_emails):
    try:
        thread_text = "\n".join([email['content'] for email in thread_emails])
        prompt = f"Summarize this email thread:\n{thread_text}"
        summary = generate_response(prompt)
        logger.debug(f"Summarized thread with {len(thread_emails)} emails")
        print(f"[DEBUG] Summarized thread with {len(thread_emails)} emails")
        return summary
    except Exception as e:
        logger.error(f"Failed to summarize thread: {str(e)}")
        print(f"[ERROR] Failed to summarize thread: {str(e)}")
        return "Summary unavailable"