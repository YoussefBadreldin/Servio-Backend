from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Dict

class ServiceException(HTTPException):
    def __init__(self, status_code: int, detail: Any = None):
        super().__init__(status_code=status_code, detail=detail)

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "path": request.url.path
        }
    )

def include_exception_handlers(app):
    app.add_exception_handler(HTTPException, http_exception_handler)