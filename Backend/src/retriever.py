# src/retriever.py
from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from src.config import RETRIEVER_THRESHOLD
import torch


from src.config import QDRANT_URL, COLLECTION_NAME, EMBEDDING_MODEL, RETRIEVER_TOPK

embeddings = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL)
client = QdrantClient(url=QDRANT_URL)

def retrieve_docs(query, top_k=RETRIEVER_TOPK, threshold=RETRIEVER_THRESHOLD):
    query_vector = embeddings.embed_query(query)
    
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True 
    )
    
    # Filter by score
    filtered_docs = [
        hit.payload for hit in search_result if hit.score >= threshold
    ]
    
    return filtered_docs
