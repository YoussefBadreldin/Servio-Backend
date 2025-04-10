import os
import json
import math
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from ...shared.exceptions import ServiceDiscoveryError
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class GuidedService:
    def __init__(self):
        """Initialize the guided service with consistent configuration."""
        self.service_registry_file = Path("data/servio_data.jsonl")
        self.faiss_index_path = Path("data/faiss_index")
        self.index_name = "servio_index"
        self.embeddings_model = "all-MiniLM-L6-v2"
        self.llm_model = "llama3-8b-8192"
        self.llm_temperature = 0.3
        self.top_k = 5
        self.min_score_threshold = 0.5
        self.chunk_size = 1000
        self.chunk_overlap = 200
        
        # Initialize components
        self.embeddings: Optional[HuggingFaceEmbeddings] = None
        self.vectorstore: Optional[FAISS] = None
        self.retriever: Optional[Any] = None
        self.chat_model: Optional[ChatGroq] = None
        
        self.initialize_components()

    def initialize_components(self) -> None:
        """Initialize all service components with error handling."""
        try:
            # Verify data file exists
            if not self.service_registry_file.exists():
                raise FileNotFoundError(f"Service registry file not found: {self.service_registry_file}")
            
            # Load documents
            self.documents = self._load_and_validate_documents()
            logger.info(f"Loaded {len(self.documents)} service registry entries")
            
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embeddings_model,
                model_kwargs={'device': 'cpu'},  # Ensure consistent device
                encode_kwargs={'normalize_embeddings': True}  # Normalize for better similarity
            )
            
            # Initialize vector store
            self.vectorstore = self._initialize_vector_store()
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={
                    "k": self.top_k,
                    "score_threshold": self.min_score_threshold
                }
            )
            
            # Initialize LLM
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
                
            self.chat_model = ChatGroq(
                temperature=self.llm_temperature,
                model_name=self.llm_model,
                api_key=groq_api_key
            )
            
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise ServiceDiscoveryError(f"Service initialization failed: {str(e)}")

    def _load_and_validate_documents(self) -> List[Document]:
        """Load and validate documents with consistent sorting and formatting."""
        documents = []
        try:
            with open(self.service_registry_file, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                
                # Sort by function name for consistency
                lines_sorted = sorted(
                    lines,
                    key=lambda x: json.loads(x).get('func_name', '').lower()
                )
                
                for line in lines_sorted:
                    data = json.loads(line)
                    
                    # Validate required fields
                    if not data.get('func_name'):
                        logger.warning(f"Skipping document missing func_name: {data}")
                        continue
                        
                    # Create consistent document format
                    content_parts = [
                        f"Service Name: {data.get('func_name', 'N/A')}",
                        f"Description: {data.get('docstring', 'No description provided')}",
                        f"Tags: {', '.join(sorted(data.get('repo', [])))}",
                        f"URL: {data.get('url', 'N/A')}"
                    ]
                    
                    documents.append(
                        Document(
                            page_content="\n".join(content_parts),
                            metadata=data
                        )
                    )
                    
            if not documents:
                raise ValueError("No valid documents found in registry")
                
            return documents
            
        except json.JSONDecodeError as e:
            raise ServiceDiscoveryError(f"Invalid JSON in registry file: {str(e)}")
        except Exception as e:
            raise ServiceDiscoveryError(f"Document loading failed: {str(e)}")

    def _initialize_vector_store(self) -> FAISS:
        """Initialize or load the FAISS vector store with validation."""
        try:
            index_file = self.faiss_index_path / f"{self.index_name}.faiss"
            
            if index_file.exists():
                logger.info("Loading existing vector store")
                return FAISS.load_local(
                    folder_path=str(self.faiss_index_path),
                    embeddings=self.embeddings,
                    index_name=self.index_name,
                    allow_dangerous_deserialization=True
                )
            else:
                logger.info("Creating new vector store")
                self.faiss_index_path.mkdir(parents=True, exist_ok=True)
                
                splitter = CharacterTextSplitter(
                    chunk_size=self.chunk_size,
                    chunk_overlap=self.chunk_overlap,
                    separator="\n",
                    length_function=len,
                    is_separator_regex=False
                )
                
                docs = splitter.split_documents(self.documents)
                
                if not docs:
                    raise ValueError("No documents available for vector store creation")
                    
                vectorstore = FAISS.from_documents(
                    documents=docs,
                    embedding=self.embeddings
                )
                
                vectorstore.save_local(
                    folder_path=str(self.faiss_index_path),
                    index_name=self.index_name
                )
                
                logger.info(f"Vector store created with {len(docs)} chunks")
                return vectorstore
                
        except Exception as e:
            raise ServiceDiscoveryError(f"Vector store initialization failed: {str(e)}")

    def _expand_query(self, query: str) -> str:
        """Expand the query with domain-specific terms for better retrieval."""
        query_lower = query.lower()
        expansions = {
            'api': 'rest graphql soap rpc',
            'gateway': 'proxy ingress load-balancer reverse-proxy',
            'microservice': 'service-mesh container orchestration',
            'cloud': 'aws azure gcp kubernetes serverless',
            'scalable': 'elastic auto-scaling high-availability',
            'integration': 'connector adapter middleware'
        }
        
        expanded = [query]
        for term, synonyms in expansions.items():
            if term in query_lower:
                expanded.append(synonyms)
                
        return ' '.join(expanded)

    def _calculate_confidences(self, scores: List[float]) -> List[float]:
        """Convert similarity scores to meaningful confidence percentages."""
        if not scores:
            return []
            
        # Normalize scores between 0.5 and 1.0 to avoid extremely low confidences
        min_score = min(scores)
        max_score = max(scores)
        range_adjusted = max(0.1, max_score - min_score)  # Prevent division by zero
        
        normalized = [
            0.5 + 0.5 * (score - min_score) / range_adjusted
            for score in scores
        ]
        
        # Softmax to convert to probabilities
        exps = [math.exp(score) for score in normalized]
        sum_exps = sum(exps)
        
        return [round(100 * (exp / sum_exps), 1) for exp in exps]

    def _format_recommendation_context(self, docs: List[Document]) -> str:
        """Format the context for LLM in a consistent way."""
        return "\n\n".join(
            f"### Service {i+1}\n"
            f"{doc.page_content}\n"
            f"Similarity Score: {score:.3f}" 
            for i, (doc, score) in enumerate(docs)
        )

    def recommend_services(self, user_query: str) -> Dict[str, Any]:
        """
        Generate service recommendations with consistent formatting.
        
        Args:
            user_query: The user's natural language query
            
        Returns:
            Dictionary containing:
            - response_text: LLM-generated explanation
            - recommendations: List of service matches
            - debug_info: Additional debugging information (optional)
        """
        try:
            if not user_query.strip():
                raise ValueError("Empty query provided")
                
            # Fresh conversation for each query
            conversation = [
                SystemMessage(content=(
                    "You are an expert software service discovery assistant. "
                    "Provide clear, concise recommendations with:\n"
                    "1. Service name\n"
                    "2. Confidence score (1-100%)\n"
                    "3. Brief explanation of relevance\n"
                    "Format as numbered list. Be specific about why each service matches."
                )),
                HumanMessage(content=user_query)
            ]
            
            # Retrieve documents with scores
            expanded_query = self._expand_query(user_query)
            retrieved_docs_with_scores: List[Tuple[Document, float]] = (
                self.vectorstore.similarity_search_with_score(
                    expanded_query,
                    k=self.top_k
                )
            )
            
            if not retrieved_docs_with_scores:
                logger.warning(f"No documents found for query: {user_query}")
                return {
                    "response_text": "No matching services found for your query.",
                    "recommendations": []
                }
            
            # Process results
            docs, scores = zip(*retrieved_docs_with_scores)
            confidences = self._calculate_confidences(list(scores))
            
            recommendations = []
            for doc, confidence, score in zip(docs, confidences, scores):
                recommendations.append({
                    "service_name": doc.metadata.get("func_name", "Unknown"),
                    "confidence": confidence,
                    "description": doc.metadata.get("docstring", ""),
                    "url": doc.metadata.get("url", ""),
                    "similarity_score": float(score)  # For debugging
                })
            
            # Generate LLM response
            context = self._format_recommendation_context(retrieved_docs_with_scores)
            
            prompt = (
                "Service Registry Matches:\n\n"
                f"{context}\n\n"
                "User Query:\n"
                f"{user_query}\n\n"
                "Provide recommendations with:\n"
                "1. Service Name\n"
                "2. Confidence %\n"
                "3. Specific reason for match\n"
                "Order by relevance. Be concise but specific."
            )
            
            conversation.append(HumanMessage(content=prompt))
            llm_response = self.chat_model.invoke(conversation)
            
            return {
                "response_text": llm_response.content,
                "recommendations": recommendations,
                "debug_info": {  # Optional debugging info
                    "expanded_query": expanded_query,
                    "raw_scores": [float(s) for s in scores]
                }
            }
            
        except Exception as e:
            logger.error(f"Recommendation error for query '{user_query}': {str(e)}")
            raise ServiceDiscoveryError(f"Recommendation failed: {str(e)}")