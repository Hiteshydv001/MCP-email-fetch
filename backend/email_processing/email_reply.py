from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config.config import Config
from utils.logger import get_logger
from database.db import save_reply
from database.models import Email
import base64
from email.mime.text import MIMEText
from ai.llm_handler import generate_response

logger = get_logger(__name__)

def create_reply(email_data, context, custom_reply=None):
    try:
        if not email_data or 'email_id' not in email_data or 'thread_id' not in email_data:
            raise ValueError("Missing required email data fields: email_id or thread_id")

        creds = Credentials.from_authorized_user_file('token.json', Config.GMAIL_API_SCOPES)
        service = build('gmail', 'v1', credentials=creds)
        
        original_email = service.users().messages().get(userId='me', id=email_data['email_id']).execute()
        sender = next((h['value'] for h in original_email['payload']['headers'] if h['name'] == 'From'), 'unknown@example.com')
        subject = next((h['value'] for h in original_email['payload']['headers'] if h['name'] == 'Subject'), 'No Subject')
        content = email_data.get('content', original_email['snippet'])

        if custom_reply:
            reply_text = custom_reply.replace('[Name]', 'Hitesh').replace('[Sender Name]', 'Hitesh')
            logger.debug(f"Using custom reply: {reply_text}")
            print(f"[DEBUG] Using custom reply: {reply_text}")
        else:
            prompt_positive = f"Generate a positive reply to this email:\nEmail: {content}\nContext: {context}"
            prompt_neutral = f"Generate a neutral reply to this email:\nEmail: {content}\nContext: {context}"
            prompt_negative = f"Generate a negative reply to this email:\nEmail: {content}\nContext: {context}"
            positive_reply = generate_response(prompt_positive)
            neutral_reply = generate_response(prompt_neutral)
            negative_reply = generate_response(prompt_negative)
            logger.debug(f"Generated reply options: Positive: {positive_reply}, Neutral: {neutral_reply}, Negative: {negative_reply}")
            print(f"[DEBUG] Generated reply options: Positive: {positive_reply}, Neutral: {neutral_reply}, Negative: {negative_reply}")
            return {
                "success": False,
                "reply_options": {
                    "positive": positive_reply,
                    "neutral": neutral_reply,
                    "negative": negative_reply
                },
                "email_id": email_data['email_id'],
                "thread_id": email_data['thread_id'],
                "sender": sender,
                "subject": subject
            }

        message = MIMEText(reply_text)
        message['to'] = sender
        message['subject'] = f"Re: {subject}"
        message['In-Reply-To'] = email_data['email_id']
        message['References'] = email_data['email_id']
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        response = service.users().messages().send(userId='me', body={'raw': raw, 'threadId': email_data['thread_id']}).execute()
        
        reply_email = Email(
            email_id=response['id'],
            sender="me",
            subject=f"Re: {subject}",
            content=reply_text,
            timestamp=response.get('timestamp', "Thu, 13 Mar 2025 23:46:36 +0530"),
            thread_id=email_data['thread_id']
        )
        saved_reply = save_reply(reply_email.to_dict())
        
        logger.info(f"Sent and saved reply for email: {email_data['email_id']} to {sender}")
        print(f"[INFO] Sent and saved reply for email {email_data['email_id']} to {sender}")
        return {"success": True, "reply_text": reply_text, "message_id": response['id']}

    except Exception as e:
        error_message = f"Failed to send reply: {str(e)}"
        logger.error(error_message, exc_info=True)
        print(f"[ERROR] {error_message}")
        return {"error": error_message}