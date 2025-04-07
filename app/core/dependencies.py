# app/core/dependencies.py
from fastapi import Depends, HTTPException, status
from typing import Optional

def get_query_token(token: Optional[str] = None):
    if token != "secret":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication token"
        )
    return token