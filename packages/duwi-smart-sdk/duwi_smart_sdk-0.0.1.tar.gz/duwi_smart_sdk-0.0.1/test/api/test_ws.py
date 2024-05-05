import asyncio

import pytest

from duwi_smart_sdk.api.ws import DeviceSynchronizationWS


def p():
    print("p")


@pytest.mark.asyncio
async def test_ws():
    ws = DeviceSynchronizationWS(
        on_callback=None,
        app_key="2e479831-1fb7-751e-7017-7534f7f99fc1",
        app_secret="26af4883a943083a4c34083897fcea10",
        access_token="715d1c63-85c0-4d74-9a89-5a0aa4806f74",
        refresh_token="c539ec1b-99d9-44f2-8bb0-b942545c0aca",
        house_no="test",
    )
    await ws.reconnect()
    keep_alive = asyncio.create_task(ws.keep_alive())
    listen = asyncio.create_task(ws.listen())

    # 等待所有任务完成
    await asyncio.gather(keep_alive, listen)

