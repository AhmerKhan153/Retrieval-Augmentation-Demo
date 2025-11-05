# src/llm.py
from langchain_ollama import OllamaLLM
from src.prompts import answer_prompt
from src.config import LLM_MODEL
from langchain.memory import (
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
    CombinedMemory
)
from langchain.chains import LLMChain

short_memory = ConversationBufferWindowMemory(
        k=5,  
        memory_key="history",
        input_key="input",
        return_messages=False
    )

def call_llm_with_context(question, docs):

    context = ""
    for doc in docs:
        context += f"Issue: {doc.get('page_content')}\n"
        context += f"Resolution: {doc.get('metadata').get('resolution', '')}\n\n"

    # Short-term memory: Last 3 Q&A pairs
    combined_memory = CombinedMemory(memories=[short_memory])
    prompt = answer_prompt

    # Creating a conversation chain
    conversation = LLMChain(
        llm= OllamaLLM(model=LLM_MODEL),
        memory=combined_memory,
        verbose=True,
        prompt = prompt
    )

    inputs = {
        "input": question,
        "context": context,
        "short_memory": short_memory.load_memory_variables({})["history"],
    }

    response = conversation.run(**inputs)
    return response 
    

   

    
    return llm.invoke(prompt)