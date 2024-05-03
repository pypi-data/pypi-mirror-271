import haitch as H
from fastapi import APIRouter, Form, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse

from poaster import dependencies
from poaster.core import components

from . import components as local_components

router = APIRouter()


@router.get("/login")
async def handle_display_login_page(
    username: dependencies.UsernameFromSessionCookie,
) -> Response:
    """Defines web endpoint for displaying the login page."""
    if username:
        return RedirectResponse("/posts", status_code=status.HTTP_302_FOUND)

    content = H.main(local_components.login_form())

    page = components.page(content, title="Login", username=username)

    return HTMLResponse(str(page))


@router.post("/login")
async def handle_login(
    access_service: dependencies.AccessService,
    username: str = Form(...),
    password: str = Form(...),
) -> Response:
    """Defines web endpoint for authenticating user credentials."""
    user = await access_service.authenticate(username, password)

    if user is None:
        return RedirectResponse("/login/failed", status_code=status.HTTP_302_FOUND)

    response = RedirectResponse("/posts", status_code=status.HTTP_302_FOUND)
    response.set_cookie("session", access_service.create_access_token(user.username))

    return response


@router.get("/logout")
async def handle_logout() -> Response:
    """Defines web endpoint for authenticating user credentials."""
    response = RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session")
    return response


@router.get("/login/failed")
async def handle_display_login_failed() -> HTMLResponse:
    """Defines web endpoint for displaying the login failure."""
    content = H.main(
        components.message("Failed to login.", variant="danger"),
        local_components.login_form(),
    )

    page = components.page(content, title="Login Failed")

    return HTMLResponse(str(page))
