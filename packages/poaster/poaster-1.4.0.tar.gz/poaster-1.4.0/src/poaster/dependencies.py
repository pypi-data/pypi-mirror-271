from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import APIKeyCookie, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

import poaster.access.repository
import poaster.access.services
import poaster.bulletin.repository
import poaster.bulletin.services
from poaster.core import exceptions, http_exceptions, oauth, sessions

AuthBearer = Annotated[oauth.Token, Depends(oauth.oauth2_scheme)]
AuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]
SessionCookie = Annotated[
    oauth.Token, Depends(APIKeyCookie(name="session", auto_error=False))
]


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session, commiting changes before closing."""
    async with sessions.async_session() as session:
        yield session
        await session.commit()


DBSession = Annotated[AsyncSession, Depends(get_db_session)]


def get_access_service(db: DBSession) -> poaster.access.services.AccessService:
    """Instantiate user repository session."""
    return poaster.access.services.AccessService.from_session(db)


AccessService = Annotated[
    poaster.access.services.AccessService, Depends(get_access_service)
]


def get_bulletin_service(db: DBSession) -> poaster.bulletin.services.BulletinService:
    """Instantiate bulletin application service."""
    return poaster.bulletin.services.BulletinService.from_session(db)


BulletinService = Annotated[
    poaster.bulletin.services.BulletinService, Depends(get_bulletin_service)
]


def get_username_from_bearer_token(token: AuthBearer) -> str:
    """Try and retrieve username based on passed token."""
    try:
        payload = oauth.decode_token(token)
    except exceptions.Unauthorized as err:
        raise http_exceptions.InvalidCredentials from err
    else:
        return str(payload.get("sub", ""))


UsernameFromBearerToken = Annotated[str, Depends(get_username_from_bearer_token)]


def get_username_from_session_cookie(user_session: SessionCookie) -> str:
    """Try and retrieve username from session cookie."""
    if user_session is None:
        return ""
    try:
        payload = oauth.decode_token(user_session)
    except exceptions.Unauthorized:
        return ""
    else:
        return str(payload.get("sub", ""))


UsernameFromSessionCookie = Annotated[str, Depends(get_username_from_session_cookie)]
