import asyncio
import json
import logging
import traceback

import websockets

from duwi_smart_sdk.const.status import Code
from duwi_smart_sdk.api.refresh_token import AuthTokenRefresherClient
from duwi_smart_sdk.const.const import WS_URL
from duwi_smart_sdk.util.sign import md5_encrypt, sha256_base64
from duwi_smart_sdk.util.timestamp import current_timestamp

_LOGGER = logging.getLogger(__name__)


class DeviceSynchronizationWS:
    def __init__(self, on_callback: callable, app_key: str, app_secret: str, access_token: str,
                 refresh_token: str, house_no: str):
        self._on_callback = on_callback
        self._server_uri = WS_URL
        self._app_key = app_key
        self._app_secret = app_secret
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._house_no = house_no
        self._connection = None

    async def connect(self):
        _LOGGER.info(f"ws connect {self._server_uri}")
        self._connection = await websockets.connect(self._server_uri)

    async def send(self, message):
        _LOGGER.info(f"ws send {message}")
        if self._connection:
            await self._connection.send(message)

    async def disconnect(self):
        if self._connection:
            await self._connection.close()

    async def reconnect(self):
        _LOGGER.info("ws reconnect --------------")
        await self.connect()
        await self.link()
        await self.bind()

    async def listen(self):
        while True:
            try:
                await self.process_messages()
            except websockets.exceptions.ConnectionClosedError:
                _LOGGER.warning('Connection closed, trying to reconnect...')
                await self.reconnect()
                await asyncio.sleep(5)

    async def link(self):
        timestamp = current_timestamp()
        client_id = md5_encrypt(timestamp)

        data = {
            "clientID": client_id,
            "appKey": self._app_key,
            "time": str(current_timestamp()),
            "sign": sha256_base64(client_id, self._app_key, timestamp, self._app_secret),
        }
        json_string = json.dumps(data)
        await self.send(
            'LINK|' + json_string
        )

    async def bind(self):
        data = {
            "accessToken": self._access_token,
            "houseNo": self._house_no,
        }
        json_string = json.dumps(data)
        await self.send(
            'BIND|' + json_string
        )

    async def refresh_token(self):
        auth = AuthTokenRefresherClient(app_key=self._app_key, app_secret=self._app_secret)
        while True:
            status, token = await auth.refresh(
                refresh_token=self._refresh_token)
            if status == Code.Success.value:
                self._access_token = token.access_token
                self._refresh_token = token.refresh_token
            await asyncio.sleep(432000)

    async def keep_alive(self):
        while True:
            try:
                await self.send('KEEPALIVE')
                await asyncio.sleep(20)
            except websockets.exceptions.ConnectionClosedError:
                _LOGGER.info('Connection closed, trying to reconnect...')
                await self.reconnect()

    async def process_messages(self):
        async for message in self._connection:
            try:
                if message == "KEEPALIVE":
                    continue
                _LOGGER.info(f"ws接受消息:{message}")
                message = str.replace(message, "&excision&", "")
                self._on_callback(message)
            except Exception as e:
                _LOGGER.error(f"ws接受消息出现异常:{e}")
                _LOGGER.error(f"error message detail: \n{traceback.format_exc()}")

            # try:
            #     if message == "KEEPALIVE":
            #         continue

            #     _LOGGER.info(f"replace message is :{message}")
            #     flag, device_no, domain, action, attrs = trans(self.hass, self._instance_id, message)
            #     if not flag:
            #         _LOGGER.warning(f"flag is not true {flag} reason is {domain}")
            #         continue
            #     await self.hass.services.async_call(domain, action, attrs)
            # except Exception as e:
            #     _LOGGER.error(f"ws accept error: {e}")
            #     _LOGGER.error(f"error message detail: \n{traceback.format_exc()}")
            # finally:
            #     if device_no:
            #         self.hass.data[DUWI_DOMAIN][self._instance_id]["LOCK"][device_no] = False
