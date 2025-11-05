from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

embedder = SentenceTransformer('intfloat/e5-base-v2')
qdrant = QdrantClient(host="localhost", port=6333)
score_threshold = 0.8  

def search_jira(query, top_k=5):
    query_vector = embedder.encode(query).tolist()
    results = qdrant.search(collection_name="jira_incidents", query_vector=query_vector, limit=top_k, with_payload=True)

    for res in results:
            #print(res.payload);
        #if res.score <= score_threshold:
            print(f"Text: {res.payload['text']}, Summary: {res.payload['summary']},Description: {res.payload['description']},  Score: {res.score:.4f}")

if __name__ == "__main__":
    user_query = input("Enter your Jira query: ")
    search_jira(user_query)