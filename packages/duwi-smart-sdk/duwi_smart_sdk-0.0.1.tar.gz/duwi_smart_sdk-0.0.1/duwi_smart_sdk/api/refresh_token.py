import json

from duwi_smart_sdk.const.const import URL
from duwi_smart_sdk.util.http import put
from duwi_smart_sdk.const.status import Code
from duwi_smart_sdk.util.sign import md5_encrypt
from duwi_smart_sdk.util.timestamp import current_timestamp
from duwi_smart_sdk.model.resp.auth import AuthToken


class AuthTokenRefresherClient:
    def __init__(self, app_key: str, app_secret: str):
        self._url = URL
        self._app_key = app_key
        self._app_secret = app_secret

    async def refresh(self, refresh_token: str) -> tuple[str, AuthToken | None]:
        body = {
            "refreshToken": refresh_token,
        }

        body_string = json.dumps(body, separators=(',', ':'))
        sign = md5_encrypt(body_string + self._app_key + str(current_timestamp()))

        headers = {
            'Content-Type': 'application/json',
            'appkey': self._app_key,
            'secret': self._app_secret,
            'time': current_timestamp(),
            'sign': sign
        }

        status, message, res = await put(self._url + "/account/token", headers, body)
        if status == Code.Success.value:
            return status, AuthToken(
                access_token=res.get("accessToken"),
                access_token_expire_time=res.get("accessTokenExpireTime"),
                refresh_token=res.get("refreshToken"),
                refresh_token_expire_time=res.get("refreshTokenExpireTime")
            )
        else:
            return status, None
