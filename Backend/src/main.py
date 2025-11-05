from src.rules import load_domain_rules, match_rule
from src.retriever import retrieve_docs
from src.reranker import rerank
from src.llm import call_llm_with_context
from src.config import FALLBACK_MESSAGE

def answer_query(query):
    # Step 1: Domain rule match
    rules = load_domain_rules()
    rule_response = match_rule(query, rules)
    if rule_response:
        return rule_response

    # Step 2: Retrieve candidates
    retrieved_docs = retrieve_docs(query)

    # if not retrieved_docs:
    #     return FALLBACK_MESSAGE

    # Step 3: Rerank
    reranked_docs = rerank(query, retrieved_docs)
    
    # Step 4: Call LLM
    return call_llm_with_context(query, reranked_docs)

if __name__ == "__main__":
    while True:
        #user_query = input("\nEnter your question (or type 'exit'): ")
        print("Bot:", answer_query("I am facing OTP error on refund screen"))
        print("Bot:", answer_query("Can you tell me why?"))
        print("Bot:", answer_query("Please Expedite the process"))
        break

        if user_query.lower() == "exit":
            break
        print(answer_query(user_query))