import base64
import hashlib
import hmac


def md5_encrypt(input_string: str) -> str:
    # 创建一个 MD5 加密对象
    md5 = hashlib.md5()

    # 更新对象内容为要加密的字符串（需先转换为 bytes 类型）
    md5.update(input_string.encode('utf-8'))

    # 获取加密后的结果（以 16 进制表示）
    encrypted_string = md5.hexdigest()

    return encrypted_string


def sha256_base64(client_id: str, app_key: str, time: str, secret_key: str) -> str:
    # 将 client_id、app_key 和 time 组合成一个字符串
    message = f"{client_id}{app_key}{time}"

    # 使用 HMAC SHA-256 加密，并获取加密结果的字节流
    hmac_result = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()

    # 对加密结果的字节流进行 Base64 编码
    sign = base64.b64encode(hmac_result).decode()

    return sign
