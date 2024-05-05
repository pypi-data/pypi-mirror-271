import pytest

from duwi_smart_sdk.api.control import ControlClient
from duwi_smart_sdk.model.req.device_control import ControlDevice


@pytest.mark.asyncio
async def test_control():
    cc = ControlClient(
        app_key="2e479831-1fb7-751e-7017-7534f7f99fc1",
        app_secret="26af4883a943083a4c34083897fcea10",
        access_token="715d1c63-85c0-4d74-9a89-5a0aa4806f74",
    )
    cd = ControlDevice(
        device_no="11900000003-5",
        house_no="c7bf567d-225a-4533-ab72-5dc080b794f5"
    )
    cd.add_param_info("switch", "on")
    status = await cc.control(cd)
    assert status == "10000"
