import time
import jwt

SECRET_KEY:str = "shu-yx-token"
ALGORITHM = "HMAC256"

# 创建token
# 接受一个字典，返回一个token
def createToken(payload:dict):
    # 设置过期时间为一个小时后
    payload["exp"] = int(time.time()) + 60 * 60  # 一个小时过期
    # 生成JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def tookenIsRight(token:str) -> bool:
    try:
        # 解码JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except jwt.ExpiredSignatureError:
        # Token过期
        return False
    except jwt.InvalidTokenError:
        # Token无效
        return False
