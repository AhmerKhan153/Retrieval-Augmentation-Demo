import csv
import re
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()  # lowercase
    text = re.sub(r'\s+', ' ', text)  # collapse whitespace
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    return text.strip()

# Load your Jira CSV data and combine + preprocess summary + description
def load_jira_data(csv_filepath):
    jira_records = []
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            combined_text = f"{row['summary']}. {row['description']}"
            cleaned_text = preprocess_text(combined_text)
            jira_records.append({
                "id": int(row['id']),
                "page_content": cleaned_text,
                "metadata": {
                    "summary": row['summary'],
                    "description": row['description'],
                    "status": row['status'],
                    "resolution": row['resolution']
                }
            })
    return jira_records

# Initialize embedding model
embedding_model = SentenceTransformer('intfloat/e5-base-v2')

# Connect to Qdrant
qdrant = QdrantClient(url="http://localhost:6333")

# Create/recreate collection with correct vector size & distance metric
qdrant.recreate_collection(
    collection_name="jira_incidents",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

# Ingest data with embeddings into Qdrant
def ingest_data(jira_records):
    points = []
    for record in jira_records:
        vector = embedding_model.encode(record["page_content"]).tolist()
        points.append(
            PointStruct(
                id=record["id"],
                vector=vector,
                payload={
                    "page_content": record["page_content"],
                    "metadata": record["metadata"]
                }
                
            )
        )
    qdrant.upsert(collection_name="jira_incidents", points=points, wait=True,)
    print(f"Ingested {len(points)} Jira incidents into Qdrant.")

if __name__ == "__main__":
    csv_file = "jira_incidents.csv"
    jira_data = load_jira_data(csv_file)
    ingest_data(jira_data)