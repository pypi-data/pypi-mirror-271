import asyncio
import logging

import poaster.access.repository
import poaster.access.schemas
import poaster.access.services
import poaster.bulletin.repository
import poaster.bulletin.schemas
import poaster.bulletin.services
from poaster.core import exceptions, sessions


async def load_fixtures():
    """Load test fixtures useful for local development."""
    async with sessions.async_session() as session:
        access_svc = poaster.access.services.AccessService.from_session(session)
        bulletin_svc = poaster.bulletin.services.BulletinService.from_session(session)

        await add_dummy_user(access_svc)
        await add_dummy_posts(bulletin_svc)


async def add_dummy_user(access_svc: poaster.access.services.AccessService):
    try:
        await access_svc.register_user(username="dummy", password="password")
    except exceptions.AlreadyExists:
        logging.info("'dummy' user already exists with password equal to 'password'.")
    else:
        logging.info("Added 'dummy' user with password equal to 'password'.")


async def add_dummy_posts(bulletin_svc: poaster.bulletin.services.BulletinService):
    async def add_post(title: str, text: str):
        await bulletin_svc.create_post(
            username="dummy",
            payload=poaster.bulletin.schemas.PostInputSchema(title=title, text=text),
        )

    await add_post("Penguins", "Penguins are a group of aquatic flightless birds.")
    await add_post("Tigers", "Tigers are the largest living cat species.")
    await add_post("Koalas", "Koala is is native to Australia.")

    logging.info("Added example dummy posts about animals.")


if __name__ == "__main__":
    asyncio.run(load_fixtures())
