# app/core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional

api_key_header = APIKeyHeader(name="X-API-KEY")

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "servio-secret-key":  # In production, use proper auth
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key