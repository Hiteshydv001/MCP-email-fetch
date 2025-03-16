from pymongo import MongoClient
from config.config import Config
from utils.logger import get_logger
from bson.objectid import ObjectId

logger = get_logger(__name__)

client = MongoClient(Config.MONGO_URI)
db = client.get_database()
emails_collection = db.emails
replies_collection = db.replies
users_collection = db.users

def save_email(email_data):
    try:
        result = emails_collection.insert_one(email_data)
        email_data['_id'] = str(result.inserted_id)
        logger.debug(f"Saved email with ID: {result.inserted_id}")
        print(f"[DEBUG] Saved email: {email_data['email_id']}")
        return email_data
    except Exception as e:
        logger.error(f"Failed to save email: {str(e)}")
        print(f"[ERROR] Failed to save email: {str(e)}")
        raise

def save_reply(reply_data):
    try:
        result = replies_collection.insert_one(reply_data)
        reply_data['_id'] = str(result.inserted_id)
        logger.debug(f"Saved reply with ID: {result.inserted_id}")
        print(f"[DEBUG] Saved reply: {reply_data['email_id']}")
        return reply_data
    except Exception as e:
        logger.error(f"Failed to save reply: {str(e)}")
        print(f"[ERROR] Failed to save reply: {str(e)}")
        raise

def get_email_by_id(email_id):
    try:
        email = emails_collection.find_one({"email_id": email_id})
        if email:
            email['_id'] = str(email['_id'])
        logger.debug(f"Retrieved email: {email_id}")
        print(f"[DEBUG] Retrieved email: {email_id}")
        return email
    except Exception as e:
        logger.error(f"Failed to get email {email_id}: {str(e)}")
        print(f"[ERROR] Failed to get email {email_id}: {str(e)}")
        raise

def get_thread(thread_id):
    try:
        thread = list(emails_collection.find({"thread_id": thread_id}).sort("timestamp", 1))
        for email in thread:
            email['_id'] = str(email['_id'])
        logger.debug(f"Retrieved thread: {thread_id}, count: {len(thread)}")
        print(f"[DEBUG] Retrieved thread {thread_id} with {len(thread)} emails")
        return thread
    except Exception as e:
        logger.error(f"Failed to get thread {thread_id}: {str(e)}")
        print(f"[ERROR] Failed to get thread {thread_id}: {str(e)}")
        raise