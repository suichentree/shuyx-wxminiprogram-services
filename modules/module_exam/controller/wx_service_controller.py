from fastapi import APIRouter
from config.log_config import logger
from utils.response_util import ResponseUtil
import requests
import json

# 创建路由实例
router = APIRouter(prefix='/mp/wxservice', tags=['mp_wxservice接口'])

# 微信小程序应用ID和应用密钥
APP_ID:str = "wxf9788c249032b959"
APP_SECRET:str = "c69674e1cb73d754ef9cab64f3553867"

async def getOpenIdByWX(code:str):
    """
    调用微信小程序登录接口,通过微信小程序登录凭证（code）获取用户OpenID
    """
    logger.info(f"调用微信小程序登录接口,通过微信小程序登录凭证（code）获取用户OpenID, code = {code}")
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={APP_ID}&secret={APP_SECRET}&js_code={code}&grant_type=authorization_code"
    # 发送GET请求，调用接口
    response = requests.get(url)
    # 获取响应结果
    response_info = json.loads(response.text)
    return ResponseUtil.success(data=response_info)

@router.get("/getAccessToken")
async def getAccessToken():
    """
    调用微信小程序登录接口,获取访问令牌（access_token）
    """
    logger.info(f"调用微信小程序登录接口,获取访问令牌（access_token） /mp/wxservice/getAccessToken")
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    # 发送GET请求，调用接口
    response = requests.get(url)
    # 获取响应结果
    response_info = json.loads(response.text)
    return ResponseUtil.success(data=response_info)