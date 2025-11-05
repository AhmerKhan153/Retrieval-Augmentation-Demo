from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from rapidfuzz import fuzz, process
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder


def load_domain_rules():
    return [
        {"text": "payment failed", "response": "Payment failed due to gateway/network issues."},
        {"text": "login locked out", "response": "User locked out after multiple failed login attempts."},
    ]

def match_rule_fuzzy(query, rules, threshold=80):
    for rule in rules:
        score = fuzz.token_set_ratio(query, rule["text"])
        if score >= threshold:
            return rule["response"]
    return None



def build_success_prompt(docs, question):
    context = ""
    for i, doc in enumerate(docs):
        summary = doc.payload.get('page_content').strip()
        resolution = doc.payload.get('metadata').get("resolution", "No resolution available").strip()
        context += (
            f"Summary: {summary}\n"
            f"Resolution: {resolution}\n\n"
        )

    successPrompt = f"""
    You are a GDRFA support assistant.  
    Answer concisely, correctly, and in a helpful tone.  
    Respond as if you already know the answer — do NOT mention the context or how you derived the answer.  
    Do NOT start with phrases like "According to the context", "Based on the information", or similar.  
    If the information provided is insufficient, reply exactly:  
    "I could not find any relevant information for your query. Please contact support for assistance."  
    Do not ask for personal information.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    return successPrompt.strip()


def apply_reranker(question, candidates):

    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

    # Extract texts from Qdrant hits
    pairs = [(question, hit.payload["page_content"]) for hit in candidates]

    # Rerank
    scores = reranker.predict(pairs)
    score_map = {doc.id: float(score) for doc, score in zip(candidates, scores)}

    THRESHOLD = -5
    filtered_docs = [doc for doc in candidates if score_map[doc.id] >= THRESHOLD]
    
    # Sort by rerank score descending
    filtered_docs.sort(key=lambda d: score_map[d.id], reverse=True)

    return filtered_docs

def call_llm_with_context(question):

    embedding_model = SentenceTransformer('intfloat/e5-base-v2')

    # Connect to Qdrant
    client = QdrantClient(url="http://localhost:6333")

    query_vector = embedding_model.encode(question).tolist()

    search_results = client.search(
        collection_name="jira_incidents",
        query_vector=query_vector,
        limit=5,
        with_payload=True,
    )
    

    reranked_results = apply_reranker(question,search_results)
    prompt = build_success_prompt(reranked_results, question)

    # LLM
    llm = OllamaLLM(model="gemma:2b")
    response = llm(prompt)
    return response.strip()

if __name__ == "__main__":
    #question = "OTP is not sending at the time of refund, what is wrong ?" #OTP refund data id# 3026 reelvance
    #question = "Why my account is locked i am unable to login now ?" # Fuzzy Logic Testing Query
    #question = "My application is stuck in in process state"  #OTP refund data id# 3015 reelvance
    question = "When will my refund process by itself ?"

    rules = load_domain_rules()
    rule_answer = match_rule_fuzzy(question, rules)

    if rule_answer:
        final_answer = rule_answer
    else:
        final_answer = call_llm_with_context(question)

    print(final_answer)


