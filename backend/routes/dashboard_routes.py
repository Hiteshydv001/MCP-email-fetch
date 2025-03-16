from flask import Blueprint, jsonify
from database.db import emails_collection, replies_collection
from utils.logger import get_logger
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)
logger = get_logger(__name__)

def clean_key(key):
    """Extracts the core sentiment/urgency value from verbose descriptions."""
    if key:
        return key.split('.')[0].strip()  # Takes text before first period
    return "Unknown"

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    try:
        # Total counts
        email_count = emails_collection.count_documents({})
        reply_count = replies_collection.count_documents({})

        # Unread emails
        unread_count = emails_collection.count_documents({"sentiment": {"$exists": False}})

        # Sentiment breakdown
        sentiment_counts = emails_collection.aggregate([
            {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
        ])
        sentiment_stats = {clean_key(doc['_id']): doc['count'] for doc in sentiment_counts if doc['_id']}

        # Urgency breakdown
        urgency_counts = emails_collection.aggregate([
            {"$group": {"_id": "$urgency", "count": {"$sum": 1}}}
        ])
        urgency_stats = {clean_key(doc['_id']): doc['count'] for doc in urgency_counts if doc['_id']}

        # Recent activity (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_emails = emails_collection.count_documents({"timestamp": {"$gte": seven_days_ago.isoformat()}})
        recent_replies = replies_collection.count_documents({"timestamp": {"$gte": seven_days_ago.isoformat()}})

        # Thread stats
        thread_count = len(emails_collection.distinct("thread_id"))

        dashboard_data = {
            "email_count": email_count,
            "reply_count": reply_count,
            "unread_count": unread_count,
            "sentiment_stats": sentiment_stats,
            "urgency_stats": urgency_stats,
            "recent_activity": {
                "emails_last_7_days": recent_emails,
                "replies_last_7_days": recent_replies
            },
            "thread_count": thread_count
        }

        logger.info(f"Dashboard data retrieved: {dashboard_data}")
        print(f"[INFO] Dashboard data retrieved: {dashboard_data}")
        return jsonify(dashboard_data)
    except Exception as e:
        logger.error(f"Failed to retrieve dashboard data: {str(e)}", exc_info=True)
        print(f"[ERROR] Failed to retrieve dashboard data: {str(e)}")
        return jsonify({"error": str(e)}), 500