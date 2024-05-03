import haitch as H
from fastapi import APIRouter, Form, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse

from poaster import dependencies
from poaster.bulletin import schemas
from poaster.core import components, http_exceptions

from . import components as local_components

router = APIRouter()


@router.get("/")
async def handle_homepage() -> Response:
    """Redirect user to posts page when the call root path."""
    return RedirectResponse("/posts", status_code=status.HTTP_302_FOUND)


@router.get("/posts")
async def handle_post_list(
    username: dependencies.UsernameFromSessionCookie,
    bulletin_service: dependencies.BulletinService,
) -> Response:
    """Defines web endpoint for displaying the login page."""
    content = H.main(
        await local_components.post_list(bulletin_service),
    )

    page = components.page(content, title="Post List", username=username)

    return HTMLResponse(str(page))


@router.get("/posts/new")
async def handle_post_new_page(
    username: dependencies.UsernameFromSessionCookie,
) -> Response:
    """Defines web endpoint for displaying new post to add."""
    if not username:
        raise http_exceptions.Forbidden

    content = H.main(local_components.post_form_new())

    page = components.page(content, title="Post New", username=username)

    return HTMLResponse(str(page))


@router.post("/posts/new")
async def handle_post_new(
    username: dependencies.UsernameFromSessionCookie,
    bulletin_service: dependencies.BulletinService,
    title: str = Form(...),
    text: str = Form(...),
) -> Response:
    """Defines web endpoint for handling new post."""
    if not username:
        raise http_exceptions.Forbidden

    await bulletin_service.create_post(
        username=username,
        payload=schemas.PostInputSchema(title=title, text=text),
    )

    return RedirectResponse("/posts", status_code=status.HTTP_302_FOUND)


@router.get("/posts/{id}")
async def handle_post_detail(
    id: int,
    username: dependencies.UsernameFromSessionCookie,
    bulletin_service: dependencies.BulletinService,
) -> Response:
    """Defines web endpoint for displaying post detail."""
    if (post := await bulletin_service.get_post(id=id)) is None:
        raise http_exceptions.NotFound

    content = H.main(
        await local_components.post_detail(bulletin_service, post, username)
    )

    page = components.page(content, title="Post Detail", username=username)

    return HTMLResponse(str(page))


@router.get("/posts/{id}/edit")
async def handle_post_edit_page(
    id: int,
    username: dependencies.UsernameFromSessionCookie,
    bulletin_service: dependencies.BulletinService,
) -> Response:
    """Defines web endpoint for displaying post to edit."""
    if not username:
        raise http_exceptions.Forbidden

    if (post := await bulletin_service.get_post(id=id)) is None:
        raise http_exceptions.NotFound

    content = H.main(local_components.post_form_edit(post))

    page = components.page(content, title="Post Edit", username=username)

    return HTMLResponse(str(page))


@router.post("/posts/{id}/edit")
async def handle_post_edit(
    id: int,
    username: dependencies.UsernameFromSessionCookie,
    bulletin_service: dependencies.BulletinService,
    title: str = Form(...),
    text: str = Form(...),
) -> Response:
    """Defines web endpoint for handling edit post."""
    if not username:
        raise http_exceptions.Forbidden

    await bulletin_service.update_post(
        id=id,
        username=username,
        payload=schemas.PostInputSchema(title=title, text=text),
    )

    return RedirectResponse(f"/posts/{id}", status_code=status.HTTP_302_FOUND)


@router.get("/posts/{id}/delete")
async def handle_post_delete_page(
    id: int,
    username: dependencies.UsernameFromSessionCookie,
    bulletin_service: dependencies.BulletinService,
) -> Response:
    """Defines web endpoint for displaying post to edit."""
    if not username:
        raise http_exceptions.Forbidden

    if (post := await bulletin_service.get_post(id=id)) is None:
        raise http_exceptions.NotFound

    content = H.main(local_components.post_form_delete(post))

    page = components.page(content, title="Post Delete", username=username)

    return HTMLResponse(str(page))


@router.post("/posts/{id}/delete")
async def handle_post_delete(
    id: int,
    username: dependencies.UsernameFromSessionCookie,
    bulletin_service: dependencies.BulletinService,
) -> Response:
    """Defines web endpoint for handling edit post."""
    if not username:
        raise http_exceptions.Forbidden

    await bulletin_service.delete_post(id=id)

    return RedirectResponse("/posts", status_code=status.HTTP_302_FOUND)
