from pymongo import MongoClient
from bson.objectid import ObjectId

class Email:
    def __init__(self, email_id, sender, subject, content, timestamp, thread_id=None, sentiment=None, urgency=None):
        self.email_id = email_id
        self.sender = sender
        self.subject = subject
        self.content = content
        self.timestamp = timestamp
        self.thread_id = thread_id
        self.sentiment = sentiment  # New: positive, negative, neutral
        self.urgency = urgency      # New: high, medium, low

    def to_dict(self):
        return {
            "email_id": self.email_id,
            "sender": self.sender,
            "subject": self.subject,
            "content": self.content,
            "timestamp": self.timestamp,
            "thread_id": self.thread_id,
            "sentiment": self.sentiment,
            "urgency": self.urgency
        }