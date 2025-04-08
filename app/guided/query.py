# SERVIO-BACKEND/app/guided/query.py
from langchain.chat_models import init_chat_model
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
import os
import math
import random

def expand_query(query: str) -> str:
    """Query expansion for better retrieval"""
    return query + " software service, microservice, API, integration, cloud service"

def recommend_services(query: str, vector_store_path: str, conversation_history: list = None):
    """Main recommendation logic"""
    # Initialize components
    embeddings = HuggingFaceEmbeddings(model_name=os.getenv("EMBEDDINGS_MODEL"))
    vector_store = FAISS.load_local(vector_store_path, embeddings)
    model = init_chat_model("llama3-8b-8192", model_provider="groq")
    
    # Initialize conversation if not provided
    if not conversation_history:
        conversation_history = [
            SystemMessage(
                content="You are a software service discovery assistant. "
                "Recommend top 5 matching services with confidence scores."
            )
        ]
    
    # Process query
    expanded_query = expand_query(query)
    conversation_history.append(HumanMessage(content=query))
    
    # Retrieve documents
    docs = vector_store.similarity_search(expanded_query, k=5)
    
    # Generate confidence scores (simulated)
    dummy_scores = [random.uniform(0.5, 1.0) for _ in docs]
    confidences = [math.exp(i)/sum(math.exp(x) for x in dummy_scores) for i in dummy_scores]
    
    # Prepare context
    context = "\n\n".join([
        f"Service {i+1}:\n{doc.page_content}\nConfidence: {conf*100:.1f}%"
        for i, (doc, conf) in enumerate(zip(docs, confidences))
    ])
    
    # Generate LLM response
    prompt = (
        "Based on these services:\n\n"
        f"{context}\n\n"
        f"Answer this query: {query}"
    )
    response = model.invoke(conversation_history + [HumanMessage(content=prompt)])
    
    return {
        "response": response.content,
        "recommendations": [
            {
                "name": doc.metadata.get("func_name", "Unknown"),
                "confidence": f"{conf*100:.1f}%",
                "description": doc.metadata.get("docstring", ""),
                "url": doc.metadata.get("url", "")
            }
            for doc, conf in zip(docs, confidences)
        ]
    }