class ServioException(Exception):
    """Base exception for Servio application"""
    pass

class ServiceDiscoveryError(ServioException):
    """Exception for service discovery failures"""
    pass

class VectorstoreException(ServioException):
    """Exception for vector store operations"""
    pass

class LLMException(ServioException):
    """Exception for LLM-related errors"""
    pass

class DirectMatchError(ServioException):
    """Exception for LLM-related errors"""
    pass