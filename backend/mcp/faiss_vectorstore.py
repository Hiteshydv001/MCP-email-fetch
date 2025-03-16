import faiss
import numpy as np
from utils.logger import get_logger

logger = get_logger(__name__)

class VectorStore:
    def __init__(self, dimension=768):
        self.index = faiss.IndexFlatL2(dimension)
        self.vectors = []
        logger.debug(f"VectorStore initialized with dimension {dimension}")
        print(f"[DEBUG] VectorStore initialized with dimension {dimension}")
    
    def add_vector(self, vector, email_id):
        try:
            self.index.add(np.array([vector]))
            self.vectors.append(email_id)
            logger.debug(f"Added vector for email {email_id}")
            print(f"[DEBUG] Added vector for email {email_id}")
        except Exception as e:
            logger.error(f"Failed to add vector for email {email_id}: {str(e)}")
            print(f"[ERROR] Failed to add vector for email {email_id}: {str(e)}")
            raise
    
    def search(self, query_vector, k=5):
        try:
            distances, indices = self.index.search(np.array([query_vector]), k)
            results = [self.vectors[i] for i in indices[0] if i < len(self.vectors)]
            logger.debug(f"Vector search returned {len(results)} results")
            print(f"[DEBUG] Vector search returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Vector search failed: {str(e)}")
            print(f"[ERROR] Vector search failed: {str(e)}")
            raise