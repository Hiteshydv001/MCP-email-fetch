from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

def get_gmail_service():
    try:
        creds = Credentials.from_authorized_user_file('token.json', Config.GMAIL_API_SCOPES)
        service = build('gmail', 'v1', credentials=creds)
        logger.debug("Gmail service initialized")
        print("[DEBUG] Gmail service initialized")
        return service
    except Exception as e:
        logger.error(f"Failed to initialize Gmail service: {str(e)}")
        print(f"[ERROR] Gmail service failed: {str(e)}")
        raise

def fetch_unread_emails():
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', q='is:unread', maxResults=5).execute()  # Limit to 5
        messages = results.get('messages', [])
        detailed_messages = []
        
        for msg in messages:
            email = service.users().messages().get(userId='me', id=msg['id']).execute()
            detailed_messages.append({
                'id': msg['id'],
                'threadId': msg['threadId'],
                'snippet': email['snippet'],
                'sender': next((h['value'] for h in email['payload']['headers'] if h['name'] == 'From'), 'Unknown'),
                'subject': next((h['value'] for h in email['payload']['headers'] if h['name'] == 'Subject'), 'No Subject'),
                'date': next((h['value'] for h in email['payload']['headers'] if h['name'] == 'Date'), 'Unknown')
            })

        logger.debug(f"Fetched {len(detailed_messages)} unread emails with details")
        print(f"[DEBUG] Fetched {len(detailed_messages)} unread emails with details")
        return detailed_messages
    except Exception as e:
        logger.error(f"Failed to fetch emails: {str(e)}")
        print(f"[ERROR] Failed to fetch emails: {str(e)}")
        raise
