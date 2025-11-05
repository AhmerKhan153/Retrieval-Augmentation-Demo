QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "jira_incidents"
EMBEDDING_MODEL = "intfloat/e5-base-v2"

RETRIEVER_TOPK = 3
RETRIEVER_THRESHOLD = 0.82

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"
RERANK_THRESHOLD = 2.5
LLM_MODEL = "gemma:7b"
FALLBACK_MESSAGE = "I could not find any relevant information for your query. Please contact support for further assistance."