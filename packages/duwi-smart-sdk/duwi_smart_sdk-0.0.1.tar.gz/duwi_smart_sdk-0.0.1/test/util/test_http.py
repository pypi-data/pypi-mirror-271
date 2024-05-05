import asyncio
from unittest import TestCase

from util.http import get
from util.timestamp import current_timestamp


class TestGet(TestCase):
    def test_get(self):
        # 定义一个运行异步测试的辅助函数
        async def run_test():
            url = "http://8.140.128.174:8019/homeApi/v1/house/infos"  # 用你想要测试的URL替换这个
            headers = {
                "Content-Type": "application/json",
                "accessToken": "715d1c63-85c0-4d74-9a89-5a0aa4806f74",
                "appkey": "2e479831-1fb7-751e-7017-7534f7f99fc1",
                "time": current_timestamp(),
                "sign": "9a83507a299c4b43cacd91568b1dc16a",
            }  # 根据需要设置请求头

            response = await get(url, headers=headers)

            # 这里写你的测试断言
            # 例如，如果你知道返回的code应该是特定值，可以这样断言:
            self.assertEqual(response[0], "10000")
            # 检查其他返回值...
            # 注意: 这个例子假定响应是个包含code, message和data的元组(Tuple)

        # 运行异步测试
        asyncio.run(run_test())