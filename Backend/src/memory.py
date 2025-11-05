import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.memory import ConversationBufferWindowMemory
from typing import Dict, List, Optional
from datetime import datetime

def __init__(self, llm, vector_db):
        # Core components
        self.llm = llm
        self.vector_db = vector_db
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Conversation tracking
        self.memory = ConversationBufferWindowMemory(
            k=5,  # Track last 5 exchanges
            memory_key="history",
            input_key="input",
            return_messages=False
        )
        
        # Configuration
        self.similarity_threshold = 0.68  # Tuned for follow-ups
        self.min_query_length = 3  # Minimum words for semantic check

def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between texts"""
        emb1 = self.embedding_model.encode(text1)
        emb2 = self.embedding_model.encode(text2)
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))