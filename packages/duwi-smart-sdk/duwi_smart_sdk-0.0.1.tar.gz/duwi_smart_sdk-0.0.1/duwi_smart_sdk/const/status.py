from enum import Enum


class Code(Enum):
    # 成功
    Success = '10000'
    # 系统错误
    SysError = '10001'
    # 账号或密码错误
    LoginError = '11000'
    # appKey异常
    AppKeyError = '99001'
    # 签名错误
    SignError = '99002'
