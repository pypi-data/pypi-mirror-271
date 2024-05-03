import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from poaster.bulletin import schemas, services


@pytest.fixture
def bulletin_service(db_session: AsyncSession) -> services.BulletinService:
    return services.BulletinService.from_session(db_session)


async def test_create_post(bulletin_service: services.BulletinService):
    got = await bulletin_service.create_post(
        username="testuser",
        payload=schemas.PostInputSchema(title="hi", text="hello, world!"),
    )
    want = schemas.PostSchema(
        id=1,
        title="hi",
        text="hello, world!",
        created_by="testuser",
        created_at=got.created_at,
    )

    assert got == want


async def test_update_post(
    db_session: AsyncSession, bulletin_service: services.BulletinService
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(qry))

    got = await bulletin_service.update_post(
        id=1,
        username="testuser",
        payload=schemas.PostInputSchema(title="hi v2", text="hello, world!!"),
    )
    want = schemas.PostSchema(
        id=1,
        title="hi v2",
        text="hello, world!!",
        created_by="testuser",
        created_at=datetime.datetime(2024, 2, 13, 8),
    )

    assert got == want


async def test_update_post_not_found(bulletin_service: services.BulletinService):
    got = await bulletin_service.update_post(
        id=42,
        username="testuser",
        payload=schemas.PostInputSchema(title="hi", text="hello, world!"),
    )
    want = None

    assert got == want


async def test_delete_post(
    db_session: AsyncSession, bulletin_service: services.BulletinService
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(qry))

    got = await bulletin_service.delete_post(id=1)
    want = schemas.PostSchema(
        id=1,
        title="hi",
        text="hello, world!",
        created_by="testuser",
        created_at=datetime.datetime(2024, 2, 13, 8),
    )

    assert got == want


async def test_delete_post_not_found(bulletin_service: services.BulletinService):
    got = await bulletin_service.delete_post(id=42)
    want = None
    assert got == want


async def test_get_post(
    db_session: AsyncSession, bulletin_service: services.BulletinService
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(qry))

    got = await bulletin_service.get_post(id=1)
    want = schemas.PostSchema(
        id=1,
        title="hi",
        text="hello, world!",
        created_by="testuser",
        created_at=datetime.datetime(2024, 2, 13, 8),
    )

    assert got == want


async def test_get_post_not_found(bulletin_service: services.BulletinService):
    got = await bulletin_service.get_post(id=42)
    want = None

    assert got == want


async def test_get_posts(
    db_session: AsyncSession, bulletin_service: services.BulletinService
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES
        ('oldest_post', 'hello, oldest_post!', 'testuser', '2024-02-13 08:00'),
        ('newest_post', 'hello, newest_post!', 'testuser', '2024-02-15 12:00')
    ;
    """
    await db_session.execute(text(qry))

    got = await bulletin_service.get_posts()
    want = [
        schemas.PostSchema(
            id=2,
            title="newest_post",
            text="hello, newest_post!",
            created_by="testuser",
            created_at=datetime.datetime(2024, 2, 15, 12, 0),
        ),
        schemas.PostSchema(
            id=1,
            title="oldest_post",
            text="hello, oldest_post!",
            created_by="testuser",
            created_at=datetime.datetime(2024, 2, 13, 8, 0),
        ),
    ]

    assert got == want


async def test_get_all_none_found(bulletin_service: services.BulletinService):
    got = await bulletin_service.get_posts()
    want = []

    assert got == want


async def test_get_latest_version_of_post(
    db_session: AsyncSession, bulletin_service: services.BulletinService
):
    add_post_qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(add_post_qry))

    add_post_versions_qry = """
    INSERT INTO post_versions (post_id, title, text, version, updated_by, updated_at)
    VALUES
      (1, 'hi v1', 'hello, world!', 1, 'testuser', '2024-02-13 08:00'),
      (1, 'hi v2', 'hello, world!!', 2, 'testuser', '2024-02-13 09:00'),
      (1, 'hi v3', 'hello, world!!!', 3, 'testuser', '2024-02-13 10:00')
    ;
    """
    await db_session.execute(text(add_post_versions_qry))

    got = await bulletin_service.get_latest_version_of_post(id=1)
    want = schemas.PostVersionSchema(
        id=3,
        post_id=1,
        title="hi v3",
        text="hello, world!!!",
        version=3,
        updated_by="testuser",
        updated_at=datetime.datetime(2024, 2, 13, 10),
    )

    assert got == want
