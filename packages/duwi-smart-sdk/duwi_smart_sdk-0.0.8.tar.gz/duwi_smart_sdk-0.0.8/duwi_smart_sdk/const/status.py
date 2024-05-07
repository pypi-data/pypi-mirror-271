from enum import Enum


class Code(Enum):
    # 成功
    SUCCESS = '10000'
    # 系统错误
    SYS_ERROR = '10001'
    # 账号或密码错误
    LOGIN_ERROR = '11000'
    # appKey异常
    APP_KEY_ERROR = '99001'
    # 签名错误
    SIGN_ERROR = '99002'
