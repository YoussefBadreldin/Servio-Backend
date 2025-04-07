from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from typing import Annotated, Optional

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def validate_api_key(api_key: Optional[str] = Depends(api_key_header)):
    from ...config.settings import settings
    
    if not settings.DEBUG and api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key

SecurityDep = Annotated[str, Depends(validate_api_key)]