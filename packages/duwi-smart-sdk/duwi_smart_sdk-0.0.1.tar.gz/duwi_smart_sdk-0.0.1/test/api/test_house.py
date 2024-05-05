import pytest

from duwi_smart_sdk.api.house import HouseInfoClient


@pytest.mark.asyncio
async def test_infos():
    hc = HouseInfoClient(
        app_key="2e479831-1fb7-751e-7017-7534f7f99fc1",
        app_secret="26af4883a943083a4c34083897fcea10",
        access_token="715d1c63-85c0-4d74-9a89-5a0aa4806f74",
    )
    status, house_infos = await hc.fetch_house_info()
    assert house_infos
