from google_auth_oauthlib.flow import InstalledAppFlow
from config.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

def get_oauth_token():
    try:
        flow = InstalledAppFlow.from_client_secrets_file('config/secrets.json', Config.GMAIL_API_SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
        logger.info("OAuth token generated and saved")
        print("[INFO] OAuth token generated and saved")
        return creds
    except Exception as e:
        logger.error(f"Failed to generate OAuth token: {str(e)}")
        print(f"[ERROR] Failed to generate OAuth token: {str(e)}")
        raise