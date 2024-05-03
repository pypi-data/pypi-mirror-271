from __future__ import annotations

import dataclasses
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from poaster.bulletin import repository, schemas
from poaster.core import exceptions


@dataclasses.dataclass(frozen=True)
class BulletinService:
    """The service layer for the bulletin domain."""

    _post_repo: repository.SupportsPostRepository
    _post_version_repo: repository.SupportsPostVersionRepository

    @classmethod
    def from_session(cls, session: AsyncSession) -> BulletinService:
        """Build bulletin service from database session."""
        return cls(
            _post_repo=repository.SqlalchemyPostRepository(session),
            _post_version_repo=repository.SqlalchemyPostVersionRepository(session),
        )

    async def create_post(
        self, *, username: str, payload: schemas.PostInputSchema
    ) -> schemas.PostSchema:
        """Create a bulletin post from an authenticated user."""
        post = await self._post_repo.create(username, payload)

        await self._post_version_repo.create(
            username=username,
            post_id=post.id,
            post=payload,
        )

        return post

    async def update_post(
        self, *, id: int, username: str, payload: schemas.PostInputSchema
    ) -> Optional[schemas.PostSchema]:
        """Get a bulletin post by id."""
        try:
            post = await self._post_repo.update(id, payload)
        except exceptions.DoesNotExist:
            return None

        await self._post_version_repo.create(
            username=username,
            post_id=post.id,
            post=payload,
        )

        return post

    async def delete_post(self, *, id: int) -> Optional[schemas.PostSchema]:
        """Get a bulletin post by id."""
        try:
            post = await self._post_repo.delete(id)
        except exceptions.DoesNotExist:
            return None
        else:
            return post

    async def get_post(self, *, id: int) -> Optional[schemas.PostSchema]:
        """Get a bulletin post by id."""
        try:
            return await self._post_repo.get_by_id(id)
        except exceptions.DoesNotExist:
            return None

    async def get_posts(self) -> list[schemas.PostSchema]:
        """Get all recipes."""
        return await self._post_repo.get_all()

    async def get_latest_version_of_post(self, *, id: int) -> schemas.PostVersionSchema:
        """Get the latest version of a bulletin post by id."""
        return await self._post_version_repo.get_latest(post_id=id)
