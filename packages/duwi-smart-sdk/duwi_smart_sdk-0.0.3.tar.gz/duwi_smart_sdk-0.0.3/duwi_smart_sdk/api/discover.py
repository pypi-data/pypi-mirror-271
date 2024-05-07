import json
import logging

from duwi_smart_sdk.model.resp.device import Device
from duwi_smart_sdk.util.http import get
from duwi_smart_sdk.const.status import Code
from duwi_smart_sdk.const.const import URL
from duwi_smart_sdk.util.sign import md5_encrypt
from duwi_smart_sdk.util.timestamp import current_timestamp

_LOGGER = logging.getLogger(__name__)


class DiscoverClient:
    def __init__(self, app_key: str, app_secret: str):
        self._url = URL
        self._app_key = app_key
        self._app_secret = app_secret

    async def discover(self, access_token: str, house_no: str) -> tuple[str, list[Device] | None]:
        body = {}
        body_string = json.dumps(body, separators=(',', ':'))

        sign = md5_encrypt(body_string + self._app_secret + str(current_timestamp()))

        headers = {
            'Content-Type': 'application/json',
            'accessToken': access_token,
            'appkey': self._app_key,
            'secret': self._app_secret,
            'time': current_timestamp(),
            'sign': sign
        }

        status, message, res = await get(self._url + f"/device/infos?houseNo={house_no}", headers, body)

        if status == Code.Success.value:
            devices = res.get("devices", [])
            devices_objects = [self._create_device_obj(device) for device in devices]
            return status, devices_objects
        else:
            return status, None

    @staticmethod
    def _create_device_obj(device_dict):
        return Device(
            device_no=device_dict.get("deviceNo", ""),
            device_name=device_dict.get("deviceName", ""),
            terminal_sequence=device_dict.get("terminalSequence", ""),
            route_num=device_dict.get("routeNum", 0),
            device_type_no=device_dict.get("deviceTypeNo", ""),
            device_sub_type_no=device_dict.get("deviceSubTypeNo", ""),
            house_no=device_dict.get("houseNo", ""),
            room_no=device_dict.get("roomNo", ""),
            is_use=device_dict.get("isUse", False),
            is_online=device_dict.get("isOnline", False),
            create_time=device_dict.get("createTime", ""),
            seq=device_dict.get("seq", 0),
            is_favorite=device_dict.get("isFavorite", False),
            favorite_time=device_dict.get("favoriteTime", ""),
            key_binding_quantity=device_dict.get("keyBindingQuantity", 0),
            key_mapping_quantity=device_dict.get("keyMappingQuantity", 0),
            value=device_dict.get("value", {})
        )
