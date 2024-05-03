from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from poaster import dependencies
from poaster.core import http_exceptions

from . import schemas

router = APIRouter(tags=["bulletin"])


@router.post(
    "/posts",
    status_code=HTTP_201_CREATED,
    summary="Creates post when passed valid input.",
)
async def handle_create_post(
    payload: schemas.PostInputSchema,
    username: dependencies.UsernameFromBearerToken,
    bulletin_service: dependencies.BulletinService,
) -> schemas.PostSchema:
    """Defines endpoint for creating bulletin posts."""
    return await bulletin_service.create_post(username=username, payload=payload)


@router.put("/posts/{id}", summary="Update post by id.")
async def handle_update_post(
    id: int,
    payload: schemas.PostInputSchema,
    username: dependencies.UsernameFromBearerToken,
    bulletin_service: dependencies.BulletinService,
) -> schemas.PostSchema:
    """Defines endpoint for updating a post."""
    post = await bulletin_service.update_post(id=id, username=username, payload=payload)

    if post is None:
        raise http_exceptions.NotFound

    return post


@router.delete("/posts/{id}", summary="Delete post by id.")
async def handle_delete_post(
    id: int,
    _: dependencies.UsernameFromBearerToken,
    bulletin_service: dependencies.BulletinService,
) -> schemas.PostSchema:
    """Defines endpoint for deleting a post."""
    if (post := await bulletin_service.delete_post(id=id)) is None:
        raise http_exceptions.NotFound

    return post


@router.get("/posts", summary="Get all posts.")
async def handle_get_posts(
    bulletin_service: dependencies.BulletinService,
) -> list[schemas.PostSchema]:
    """Defines endpoint for retrieving all posts."""
    return await bulletin_service.get_posts()


@router.get("/posts/{id}", summary="Get post by id.")
async def handle_get_post(
    id: int,
    bulletin_service: dependencies.BulletinService,
) -> schemas.PostSchema:
    """Defines endpoint for retrieving a post by its id."""
    if (post := await bulletin_service.get_post(id=id)) is None:
        raise http_exceptions.NotFound

    return post
