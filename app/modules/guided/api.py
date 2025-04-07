import os
import json
import math
import random
from typing import List, Tuple, Optional
from pathlib import Path

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from .models import RecommendationResponse, ServiceRecommendation
from app.config import settings

class ServiceDiscovery:
    def __init__(self, groq_api_key: str = None):
        """Initialize the service discovery system."""
        self.groq_api_key = groq_api_key or settings.GROQ_API_KEY
        os.environ["GROQ_API_KEY"] = self.groq_api_key
        
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.vectorstore: Optional[FAISS] = None
        self.retriever = None
        self.chat_model = init_chat_model(settings.CHAT_MODEL, model_provider="groq")
        self.conversation_history = [
            SystemMessage(
                content=(
                    "You are a software service discovery assistant. "
                    "Your task is to recommend the top 5 best matching services from a registry "
                    "based on the user's query. For each recommendation, include the service name "
                    "and a confidence probability. Use conversational context to update "
                    "recommendations on follow-up queries."
                )
            )
        ]

    def load_jsonl_data(self, file_path: str) -> List[Document]:
        """Load service registry data from JSONL file."""
        documents = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        content = (
                            f"Service Name: {data.get('func_name', 'N/A')}\n"
                            f"Description: {data.get('docstring', 'No description provided')}\n"
                            f"Tags: {', '.join(data.get('repo', []))}\n"
                            f"URL: {data.get('url', 'N/A')}"
                        )
                        documents.append(Document(page_content=content, metadata=data))
                    except json.JSONDecodeError as e:
                        print(f"Skipping invalid JSON line: {e}")
        return documents

    def load_xml_data(self, file_path: str) -> List[Document]:
        """Load service registry data from XML file."""
        import xml.etree.ElementTree as ET
        
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        documents = []
        for record in root.findall('.//record'):
            try:
                service_name = record.find('func_name').text if record.find('func_name') is not None else 'N/A'
                description = record.find('docstring').text if record.find('docstring') is not None else 'No description provided'
                tags = [tag.text for tag in record.findall('repo/tag')] if record.find('repo') is not None else []
                url = record.find('url').text if record.find('url') is not None else 'N/A'
                
                content = (
                    f"Service Name: {service_name}\n"
                    f"Description: {description}\n"
                    f"Tags: {', '.join(tags)}\n"
                    f"URL: {url}"
                )
                metadata = {
                    "func_name": service_name,
                    "description": description,
                    "tags": tags,
                    "url": url
                }
                documents.append(Document(page_content=content, metadata=metadata))
            except Exception as e:
                print(f"Error processing XML record: {e}")
                continue
        
        return documents

    def initialize_vector_store(self, documents: List[Document]):
        """Initialize the vector store with documents."""
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = splitter.split_documents(documents)
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

    def expand_query(self, query: str) -> str:
        """Simple query expansion for improved retrieval."""
        return query + " software service, microservice, API, integration, cloud service"

    def recommend_services(self, user_query: str) -> Tuple[str, List[ServiceRecommendation]]:
        """Recommend services based on user query."""
        if not self.retriever:
            raise ValueError("Vector store not initialized. Load data first.")
            
        expanded_query = self.expand_query(user_query)
        self.conversation_history.append(HumanMessage(content=user_query))
        
        retrieved_docs = self.retriever.get_relevant_documents(expanded_query)
        
        # Simulate similarity scores and convert to confidence probabilities
        dummy_scores = [random.uniform(0.5, 1.0) for _ in retrieved_docs]
        def softmax(x):
            ex = [math.exp(i) for i in x]
            sum_ex = sum(ex)
            return [i / sum_ex for i in ex]
        confidences = softmax(dummy_scores)
        
        recommendations = []
        for doc, conf in zip(retrieved_docs, confidences):
            service_name = doc.metadata.get("func_name", "Unknown Service")
            description = doc.metadata.get("description", "No description available")
            url = doc.metadata.get("url", "")
            
            recommendations.append(ServiceRecommendation(
                service_name=service_name,
                confidence=round(conf * 100, 1),
                description=description,
                url=url
            ))
        
        context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        prompt = (
            "Based on the following service registry entries:\n"
            f"{context_text}\n\n"
            "and the user's query: " + user_query + "\n\n"
            "Please provide a recommendation of the top 5 matching services with their confidence probabilities."
        )
        
        self.conversation_history.append(HumanMessage(content=prompt))
        response = self.chat_model.invoke(self.conversation_history)
        self.conversation_history.append(response)
        
        return response.content, recommendations

    def process_uml_image(self, image_path: str) -> str:
        """Process UML diagram image and generate PlantUML code."""
        try:
            from PIL import Image
            import pytesseract
            
            img = Image.open(image_path)
            extracted_text = pytesseract.image_to_string(img)
            
            prompt = (
                "You are an expert in UML diagramming and PlantUML. "
                "Given the following extracted textual information from a UML diagram, generate the complete PlantUML source code "
                "that represents the diagram. Use proper PlantUML syntax and include all relationships and annotations:\n\n"
                f"{extracted_text}\n\nPlantUML Code:"
            )
            
            response = self.chat_model.invoke([HumanMessage(content=prompt)])
            return response.content
        except ImportError:
            raise ImportError("Please install pytesseract and pillow packages for UML processing")
        except Exception as e:
            raise Exception(f"Error processing UML image: {str(e)}")