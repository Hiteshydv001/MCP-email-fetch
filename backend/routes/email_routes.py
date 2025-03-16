from flask import Blueprint, jsonify, request
from flask_cors import CORS
from email_processing.gmail_fetch import fetch_unread_emails
from email_processing.email_reply import create_reply
from mcp.mcp_retriever import retrieve_context
from database.db import save_email, get_thread
from database.models import Email
from utils.logger import get_logger

email_bp = Blueprint('email', __name__)
logger = get_logger(__name__)

# Persistent cache for reply options and context
reply_cache = {}

@email_bp.route('/emails', methods=['GET'])
def get_emails():
    try:
        emails = fetch_unread_emails()
        if not emails:
            logger.warning("No unread emails fetched")
            print(f"[WARNING] No unread emails fetched")
            return jsonify([])
        enriched_emails = []
        for email in emails:
            email_obj = Email(
                email_id=email['id'],
                sender=email['sender'],
                subject=email['subject'],
                content=email['snippet'],
                timestamp=email['date'],
                thread_id=email['threadId']
            )
            email_dict = email_obj.to_dict()
            email_dict['sentiment'] = "Pending"
            email_dict['urgency'] = "Pending"
            enriched_email = save_email(email_dict)
            enriched_emails.append(enriched_email)
        logger.info(f"Returning {len(enriched_emails)} emails")
        print(f"[INFO] Returning {len(enriched_emails)} emails")
        return jsonify(enriched_emails)
    except Exception as e:
        logger.error(f"Failed to fetch emails: {str(e)}", exc_info=True)
        print(f"[ERROR] Failed to fetch emails: {str(e)}")
        return jsonify({"error": str(e)}), 500

@email_bp.route('/reply', methods=['POST'])
def reply_to_email():
    try:
        email_data = request.json
        if not email_data or 'email_id' not in email_data or 'thread_id' not in email_data:
            raise ValueError("Missing required fields: email_id or thread_id")
        email_id = email_data['email_id']
        thread_id = email_data['thread_id']
        reply_text = email_data.get('reply_text')
        cache_key = f"{email_id}:{thread_id}"

        if reply_text:  # Send reply immediately
            context = reply_cache.get(cache_key, {}).get('context') or retrieve_context(thread_id, email_data.get('content', ''))
            result = create_reply(email_data, context, custom_reply=reply_text)
            if "error" in result:
                logger.error(f"Reply failed with error: {result['error']}")
                print(f"[ERROR] Reply failed with error: {result['error']}")
                return jsonify(result), 500
            if result['success'] and cache_key in reply_cache:
                del reply_cache[cache_key]
            return jsonify(result)
        
        # If no reply_text, check cache or generate options
        if cache_key in reply_cache:
            result = {
                "success": False,
                "reply_options": reply_cache[cache_key]['reply_options'],
                "email_id": email_id,
                "thread_id": thread_id,
                "sender": reply_cache[cache_key]['sender'],
                "subject": reply_cache[cache_key]['subject']
            }
            logger.debug(f"Using cached options for {cache_key}")
            print(f"[DEBUG] Using cached options for {cache_key}")
        else:
            context = retrieve_context(thread_id, email_data.get('content', ''))
            result = create_reply(email_data, context)
            if "error" in result:
                logger.error(f"Reply failed with error: {result['error']}")
                print(f"[ERROR] Reply failed with error: {result['error']}")
                return jsonify(result), 500
            reply_cache[cache_key] = {
                "reply_options": result['reply_options'],
                "context": context,
                "email_id": email_id,
                "thread_id": thread_id,
                "sender": result['sender'],
                "subject": result['subject']
            }
        
        logger.info(f"Reply processed for email {email_id}: {result}")
        print(f"[INFO] Reply processed for email {email_id}: {result}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to process reply: {str(e)}", exc_info=True)
        print(f"[ERROR] Failed to process reply: {str(e)}")
        return jsonify({"error": str(e)}), 500

@email_bp.route('/thread', methods=['GET'])
def get_thread_data():
    try:
        thread_id = request.args.get('thread_id')
        if not thread_id:
            raise ValueError("Missing thread_id parameter")
        thread = get_thread(thread_id)
        logger.info(f"Retrieved thread {thread_id} with {len(thread)} emails")
        print(f"[INFO] Retrieved thread {thread_id} with {len(thread)} emails")
        return jsonify(thread)
    except Exception as e:
        logger.error(f"Failed to fetch thread: {str(e)}", exc_info=True)
        print(f"[ERROR] Failed to fetch thread: {str(e)}")
        return jsonify({"error": str(e)}), 500