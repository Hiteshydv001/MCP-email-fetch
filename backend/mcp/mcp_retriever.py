import faiss
import numpy as np
from database.db import get_thread
from config.config import Config
from utils.logger import get_logger
import google.generativeai as genai  # Add this for embedding

logger = get_logger(__name__)

MCP_RETRIEVAL_TOP_K = 5
vector_store = None

def initialize_vector_store():
    global vector_store
    if vector_store is None:
        vector_store = faiss.IndexFlatL2(768)  # Dimension 768 for Gemini embeddings
        logger.debug("VectorStore initialized with dimension 768")
        print("[DEBUG] VectorStore initialized with dimension 768")

def get_embedding(content):
    try:
        genai.configure(api_key=Config.GEMINI_API_KEY)
        result = genai.embed_content(model="models/embedding-001", content=content, task_type="retrieval_document")
        vector = np.array(result['embedding'], dtype=np.float32)
        logger.debug(f"Generated embedding for content: {content[:50]}...")
        print(f"[DEBUG] Generated embedding for content: {content[:50]}...")
        return vector
    except Exception as e:
        logger.error(f"Failed to generate embedding: {str(e)}")
        print(f"[ERROR] Failed to generate embedding: {str(e)}")
        raise

def add_email_to_vector_store(email):
    try:
        vector = get_embedding(email['content'])
        vector_store.add(vector.reshape(1, -1))
        return email['email_id']
    except Exception as e:
        logger.error(f"Failed to add email to vector store: {str(e)}")
        raise

def retrieve_context(thread_id, query_content):
    try:
        initialize_vector_store()
        thread = get_thread(thread_id)
        
        # Populate vector store
        email_ids = []
        for email in thread:
            email_id = add_email_to_vector_store(email)
            email_ids.append(email_id)
        
        # Generate query vector
        query_vector = get_embedding(query_content or "default query")
        
        # Search similar emails
        distances, indices = vector_store.search(query_vector.reshape(1, -1), MCP_RETRIEVAL_TOP_K)
        similar_email_ids = [email_ids[i] for i in indices[0] if i < len(email_ids)]
        context = [email['content'] for email in thread if email['email_id'] in similar_email_ids]
        
        logger.debug(f"Retrieved context for thread {thread_id}, size: {len(context)}")
        print(f"[DEBUG] Retrieved context for thread {thread_id}, size: {len(context)}")
        return context
    except Exception as e:
        logger.error(f"Failed to retrieve context for thread {thread_id}: {str(e)}")
        print(f"[ERROR] Failed to retrieve context for thread {thread_id}: {str(e)}")
        raise