import datetime

import pydantic
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from poaster.access import schemas, services
from poaster.core import exceptions, oauth


@pytest.fixture
def access_service(db_session: AsyncSession) -> services.AccessService:
    return services.AccessService.from_session(db_session)


@pytest.fixture
async def user(access_service: services.AccessService) -> schemas.UserSchema:
    user = schemas.UserRegistrationSchema(username="bob", password="password")
    return await access_service._user_repo.create(user)


async def test_authenticate_success(
    access_service: services.AccessService, user: schemas.UserSchema
):
    got = await access_service.authenticate(user.username, "password")
    want = user

    assert got == want


async def test_authenticate_bad_username(access_service: services.AccessService):
    got = await access_service.authenticate("badusername", "password")
    want = None

    assert got == want


async def test_authenticate_bad_pw(
    access_service: services.AccessService, user: schemas.UserSchema
):
    got = await access_service.authenticate(user.username, "badpw")
    want = None

    assert got == want


def test_encoding_and_decoding_of_user_access_token(
    access_service: services.AccessService, user: schemas.UserSchema
):
    now_in_secs = int(datetime.datetime.now().strftime("%s"))

    token = access_service.create_access_token(username=user.username, minutes=1)
    payload = access_service.decode_access_token(token)

    assert payload.sub == user.username  # subject is username
    assert payload.exp - now_in_secs == 60  # expiration is 1 minute


def test_wrongly_formatted_token_raises_unauthorized(
    access_service: services.AccessService,
):
    token = oauth.Token("blahblahblahblahIamatokenhaha")

    with pytest.raises(exceptions.Unauthorized):
        access_service.decode_access_token(token)


def test_wrong_payload_field_raises_validation_error(
    access_service: services.AccessService,
):
    token = oauth.encode_token(
        {
            "sub": "bob",
            "iss": "me",  # 'iss' field is not part of the access token schema
        }
    )

    with pytest.raises(pydantic.ValidationError):
        access_service.decode_access_token(token)


@pytest.mark.parametrize(
    "creds",
    [
        pytest.param(("testuser", "password" * 100), id="password too long"),
        pytest.param(("testuser" * 100, "password"), id="username too long"),
    ],
)
async def test_register_user_validation(
    access_service: services.AccessService, creds: tuple[str, str]
):
    username, password = creds
    with pytest.raises(pydantic.ValidationError):
        await access_service.register_user(username, password)


async def test_register_user_and_list_usernames(access_service: services.AccessService):
    await access_service.register_user("testuser", "password")

    got = await access_service.list_usernames()
    want = ["testuser"]

    assert got == want


async def test_register_user_already_exists(access_service: services.AccessService):
    await access_service.register_user("testuser", "password")

    got = await access_service.check_username_exists("testuser")
    want = True

    assert got == want


async def test_check_username_does_not_exists(access_service: services.AccessService):
    await access_service.register_user("testuser", "password")

    got = await access_service.check_username_exists("baduser")
    want = False

    assert got == want


async def test_duplicate_user_registration(access_service: services.AccessService):
    await access_service.register_user("testuser", "password")
    with pytest.raises(exceptions.AlreadyExists):
        await access_service.register_user("testuser", "password")
