# app/core/exceptions.py
from fastapi import HTTPException, status

class ServioException(HTTPException):
    def __init__(self, detail: str, code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=code, detail=detail)

class NotFoundException(ServioException):
    def __init__(self, item: str):
        super().__init__(f"{item} not found", status.HTTP_404_NOT_FOUND)

class AuthException(ServioException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED)