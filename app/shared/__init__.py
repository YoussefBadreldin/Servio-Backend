# servio-backend/app/shared/__init__.py
from .exceptions import (
    ServioException,
    ServiceDiscoveryError,
    VectorstoreException,
    LLMException
)

__all__ = [
    "ServioException",
    "ServiceDiscoveryError",
    "VectorstoreException",
    "LLMException"
]