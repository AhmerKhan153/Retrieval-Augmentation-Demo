# src/reranker.py
from sentence_transformers import CrossEncoder
from src.config import RERANKER_MODEL, RERANK_THRESHOLD

cross_encoder = CrossEncoder(RERANKER_MODEL)

def rerank(query, docs):
    if not docs:
        return []
    
    pairs = [(query, doc['page_content']) for doc in docs]
    scores = cross_encoder.predict(pairs)
    
    # Attach scores back to docs
    scored_docs = [(doc, score) for doc, score in zip(docs, scores)]
    
    # Filter and sort by score
    filtered_docs = [doc for doc, score in scored_docs if score >= RERANK_THRESHOLD]
    sorted_docs = sorted(filtered_docs, key=lambda d: scores[docs.index(d)], reverse=True)
    return sorted_docs