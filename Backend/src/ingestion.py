import csv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
from src.config import QDRANT_URL, COLLECTION_NAME, EMBEDDING_MODEL
from src.preprocessing import preprocess_text

DATA_FILE = "data/jira_incidents.csv"

def load_jira_data(csv_filepath):
    records = []
    with open(csv_filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            combined = f"{row['summary']}. {row['description']}"
            cleaned = preprocess_text(combined)
            records.append({
                "id": int(row['id']),
                "page_content": cleaned,
                "metadata": dict(row)
            })
    return records

def ingest_data(records):
    qdrant = QdrantClient(url=QDRANT_URL)
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )

    embedder = SentenceTransformer(EMBEDDING_MODEL)
    points = [
        PointStruct(
            id=rec["id"],
            vector=embedder.encode(rec["page_content"]).tolist(),
            payload=rec
        )
        for rec in records
    ]
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
    print(f"Ingested {len(points)} records.")

def main():
    print("Starting ingestion...")
    jira_data = load_jira_data(DATA_FILE)
    ingest_data(jira_data)
    print("✅ Ingestion complete.")

if __name__ == "__main__":
    main()