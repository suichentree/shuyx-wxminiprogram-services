from fastapi import APIRouter, Body
from config.log_config import logger
from utils.response_util import ResponseUtil
from utils.jwt_util import JWTUtil
import time
# 创建路由实例
router = APIRouter(prefix='/mp/common', tags=['common接口'])

"""
获取token接口
"""
@router.get("/api/applet/common/token")
def get_token():
    logger.info("/api/applet/common/token,获取token")
    # 创建token载荷
    payload = {
        "userName": "shu-yx",
        "passWord": "123456",
    }
    # 生成JWT token
    token = JWTUtil.create_token(payload)
    # 返回结果
    response_data = payload
    response_data["token"] = token
    return ResponseUtil.success(data=response_data)
