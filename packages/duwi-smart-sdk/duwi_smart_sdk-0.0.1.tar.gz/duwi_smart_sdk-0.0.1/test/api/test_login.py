import pytest

from duwi_smart_sdk.api.login import LoginClient


@pytest.mark.asyncio
async def test_login():
    lc = LoginClient(app_key="2e479831-1fb7-751e-7017-7534f7f99fc1",app_secret="26af4883a943083a4c34083897fcea10")
    status, token = await lc.login("18248625125", "biaoge666")
    assert token is not None

