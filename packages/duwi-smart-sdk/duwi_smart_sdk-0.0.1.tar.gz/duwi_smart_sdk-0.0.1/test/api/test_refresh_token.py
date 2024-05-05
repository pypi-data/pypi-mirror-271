import pytest

from duwi_smart_sdk.api.refresh_token import AuthTokenRefresherClient


@pytest.mark.asyncio
async def test_refresh():
    at = AuthTokenRefresherClient(
        app_key="2e479831-1fb7-751e-7017-7534f7f99fc1",
        app_secret="26af4883a943083a4c34083897fcea10",
    )
    status, token = await at.refresh(
        refresh_token="c539ec1b-99d9-44f2-8bb0-b942545c0aca"
    )
    assert token
