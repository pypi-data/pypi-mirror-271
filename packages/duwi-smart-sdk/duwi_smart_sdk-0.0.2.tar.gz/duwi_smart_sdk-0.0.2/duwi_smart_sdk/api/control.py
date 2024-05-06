import json
from typing import Optional

from duwi_smart_sdk.util.sign import md5_encrypt
from duwi_smart_sdk.util.timestamp import current_timestamp
from duwi_smart_sdk.const.const import URL
from duwi_smart_sdk.util.http import post
from duwi_smart_sdk.model.req.device_control import ControlDevice


class ControlClient:
    def __init__(self, app_key: str, app_secret: str, access_token: str):
        self._url = URL
        self._app_key = app_key
        self._app_secret = app_secret
        self._access_token = access_token

    async def control(self, body: Optional[ControlDevice] = None) -> str:
        # 把body转换为字符串，并且删除所有的空格
        body_string = json.dumps(body.to_dict(), separators=(',', ':')) if body is not None else ""

        sign = md5_encrypt(body_string + self._app_secret + str(current_timestamp()))

        headers = {
            'Content-Type': 'application/json',
            'accessToken': self._access_token,
            'appkey': self._app_key,
            'secret': self._app_secret,
            'time': current_timestamp(),
            'sign': sign
        }

        body_dict = body.to_dict() if body is not None else None
        status, message, res = await post(self._url + "/device/batchCommandOperate", headers, body_dict)

        return status
