import json
import math
import random
from typing import List, Tuple, Optional
from pathlib import Path
from fastapi import HTTPException, UploadFile
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from ...config.settings import settings
from ...utils.file_handlers import save_uploaded_file
from .models import ServiceRecommendation, SearchQuery

class GuidedDiscoveryService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.vectorstore = None
        self.retriever = None
        self._initialize_chat_model()
    
    def _initialize_chat_model(self):
        self.conversation_history = [
            SystemMessage(
                content=(
                    "You are a software service discovery assistant. "
                    "Your task is to recommend the top 5 best matching services from a registry. "
                    "For each recommendation, include the service name and a confidence probability."
                )
            )
        ]
        self.chat_model = init_chat_model(settings.GROQ_MODEL, model_provider="groq")
    
    async def load_registry(self, file_path: str) -> bool:
        try:
            documents = []
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        content = (
                            f"Service Name: {data.get('func_name', 'N/A')}\n"
                            f"Description: {data.get('docstring', 'No description')}\n"
                            f"Tags: {', '.join(data.get('repo', []))}\n"
                            f"URL: {data.get('url', 'N/A')}"
                        )
                        documents.append(Document(page_content=content, metadata=data))
            
            splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = splitter.split_documents(documents)
            
            self.vectorstore = FAISS.from_documents(docs, self.embeddings)
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
            return True
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load registry: {str(e)}"
            )
    
    async def process_upload(self, file: UploadFile) -> bool:
        try:
            file_path = await save_uploaded_file(file, settings.DATA_DIR)
            return await self.load_registry(file_path)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"File processing failed: {str(e)}"
            )
    
    async def recommend_services(self, query: SearchQuery) -> Tuple[str, List[ServiceRecommendation]]:
        try:
            expanded_query = self._expand_query(query.query)
            self.conversation_history.append(HumanMessage(content=query.query))
            
            retrieved_docs = self.retriever.get_relevant_documents(expanded_query)
            
            recommendations = self._generate_recommendations(retrieved_docs)
            response = self._generate_llm_response(query.query, retrieved_docs)
            
            return response, recommendations
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Recommendation failed: {str(e)}"
            )
    
    def _expand_query(self, query: str) -> str:
        return query + " software service, microservice, API, integration, cloud service"
    
    def _generate_recommendations(self, docs) -> List[ServiceRecommendation]:
        dummy_scores = [random.uniform(0.5, 1.0) for _ in docs]
        confidences = self._softmax(dummy_scores)
        
        return [
            ServiceRecommendation(
                service_name=doc.metadata.get("func_name", "Unknown Service"),
                confidence=round(conf * 100, 1),
                description=doc.metadata.get("docstring", ""),
                url=doc.metadata.get("url", "")
            )
            for doc, conf in zip(docs, confidences)
        ]
    
    def _softmax(self, x):
        ex = [math.exp(i) for i in x]
        sum_ex = sum(ex)
        return [i / sum_ex for i in ex]
    
    def _generate_llm_response(self, query: str, docs) -> str:
        context_text = "\n\n".join([doc.page_content for doc in docs])
        prompt = (
            "Based on these service registry entries:\n"
            f"{context_text}\n\n"
            f"and the user's query: {query}\n\n"
            "Please provide recommendations with confidence probabilities."
        )
        
        self.conversation_history.append(HumanMessage(content=prompt))
        response = self.chat_model.invoke(self.conversation_history)
        self.conversation_history.append(response)
        
        return response.content