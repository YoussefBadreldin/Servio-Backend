# SERVIO-BACKEND/app/guided/vectorizer.py
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
from typing import List
from app.guided.processing import process_jsonl

class RegistryVectorizer:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=os.getenv("EMBEDDINGS_MODEL")
        )
        
    def vectorize_registry(self, registry_path: str) -> str:
        store_path = f"{os.getenv('VECTOR_STORE_DIR')}/{os.path.basename(registry_path)}.faiss"
        
        if os.path.exists(store_path):
            return store_path
            
        docs = process_jsonl(registry_path)
        vector_store = FAISS.from_documents(docs, self.embeddings)
        vector_store.save_local(store_path)
        return store_path