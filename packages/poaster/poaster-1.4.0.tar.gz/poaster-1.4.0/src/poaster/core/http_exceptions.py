from fastapi import HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from starlette import status

from . import components

InvalidCredentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

Forbidden = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Action not authorized",
)

NotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found.",
)


async def handle_forbidden(request: Request, exc: Exception) -> Response:
    return HTMLResponse(
        str(components.unauthorized_page()),
        status_code=status.HTTP_403_FORBIDDEN,
    )


async def handle_not_found(request: Request, exc: Exception) -> Response:
    return HTMLResponse(
        str(components.not_found_page(username="")),
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def handle_validation_error(request: Request, exc: Exception) -> Response:
    return HTMLResponse(
        str(components.not_found_page(username="")),
        status_code=status.HTTP_404_NOT_FOUND,
    )
