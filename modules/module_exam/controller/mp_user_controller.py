from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter,Body
from config.log_config import logger
from modules.module_exam.service.mp_user_service import MpUserService
from modules.module_exam.controller.wx_controller import getOpenIdByWX
from modules.module_exam.model.mp_user_model import MpUserModel
from utils.response_util import ResponseUtil
from utils.jwt_util import JWTUtil

# 创建路由实例
router = APIRouter(prefix='/mp/user', tags=['mp_user接口'])

# 创建服务实例
MpUserService_instance = MpUserService()

"""
手机号注册接口
"""
@router.get("/phoneRegister")
def phoneRegister(phone:str,password:str):
    logger.info(f'/mp/user/phoneRegister, phone = {phone} password = {password}')
    # 构造用户字典数据
    user = {
        "phone": phone,
        "password": password
    }
    # 调用服务层方法，新增用户
    result = MpUserService_instance.add(data=user)
    if result["success"]:
        return ResponseUtil.success(data={"isRegister": 1, "message": "注册成功"})
    else:
        return ResponseUtil.error(data={"isRegister": 0, "message": "注册失败"})

"""
电话登录接口
"""
@router.post("/phoneLogin")
def phoneLogin(phone:str = Body(...),password:str = Body(...)):
    logger.info(f'/mp/user/phoneLogin, phone = {phone} password = {password}')
    # 构造用户字典数据
    user = {
        "phone": phone,
        "password": password
    }
    # 调用服务层方法，新增用户
    result = MpUserService_instance.get_one_by_filters(filters=user)
    print(result)
    if result is None:
        return ResponseUtil.error(data={"userId": 0, "isLogin": 0, "message": "电话登录失败"})

    return ResponseUtil.success(data={"userId": result["id"], "isLogin": 1, "message": "电话登录成功"})

"""
重置密码
"""
@router.post("/resetPass")
def phoneLogin(phone:str = Body(...),password:str = Body(...),newpassword:str = Body(...)):
    logger.info(f'/mp/user/resetPass, phone = {phone} password = {password} newpassword = {newpassword}')
    # 构造用户字典数据
    user = {
        "phone": phone,
        "password": password
    }
    # 调用服务层方法，查询用户是否存在
    result = MpUserService_instance.get_one_by_filters(filters=user)
    if result is not None:
        # 构造需要更新的数据
        newuser = {
            "password": newpassword
        }
        newresult = MpUserService_instance.update(id=result["id"],data=newuser)
        if newresult["success"]:
            return ResponseUtil.success(data={"isReset": 1, "message": "重置密码成功"})
        else:
            return ResponseUtil.error(data={"isReset": 0,"message": "重置密码失败1"})
    else:
        return ResponseUtil.error(data={"isReset": 0,"message": "重置密码失败2"})

"""
微信登录接口
1.传入code，得到用户的openId和unionId
2.注册或登录用户
"""
@router.post("/wxLogin")
def wxLogin(code:str = Body(None),headUrl:str = Body(None),name:str = Body(None),gender:int = Body(None),address:str = Body(None)):
        logger.info(f'/mp/user/wxLogin, code = {code}, headUrl = {headUrl}, name = {name}, gender = {gender}, address = {address}')
        # 根据code获取openId和unionId
        openId:str = None
        unionId:str = None
        wxinfo = getOpenIdByWX(code)
        if wxinfo is not None:
            openId = wxinfo.get("openid")
            unionId = wxinfo.get("unionid")

        # 根据openid 查询用户是否存在
        user = MpUserService_instance.get_one_by_filters(filters={"openId": openId})
        if user is None:
            # 查询不出用户，则注册用户
            newuser = {
                "openId": openId,
                "unionId": unionId,
                "headUrl": headUrl,
                "name": name,
                "gender": gender,
                "loginCount":1,
                "lastLoginTime": datetime.now()
            }
            # 调用服务层方法，新增用户
            result = MpUserService_instance.add(model_instance=newuser)
            if result is False:
                return ResponseUtil.error(data={"message": "微信注册用户失败"})

        else:
            # 查询到用户，则用户登录
            user.loginCount += 1
            user.lastLoginTime = datetime.now()
            result = MpUserService_instance.update_by_id(id=user.id,model_instance=user)
            if result:
                return ResponseUtil.error(data={"message": "微信登录用户失败"})


        # 创建token,传入openId,userId生成token
        token = JWTUtil.create_token({"openId": openId,"userId":user.id})
        # 返回响应数据
        return ResponseUtil.success(data={"openId": openId,"userId":user.id,"token":token})

@router.post("/saveUserINFO")
def saveUserINFO(userId:int = Body(),head:str = Body(),name:str = Body(),gender:int = Body(),age = Body(),address:str = Body(),phone = Body(),email = Body()):
        logger.info(f'/mp/user/saveUserINFO, userId = {userId} head = {head} name = {name} gender = {gender} age = {age} address = {address} phone = {phone} email = {email}')
        updateuser = {
            "id": userId,
            "head": head,
            "name": name,
            "gender": gender,
            "age": age,
            "address": address,
            "phone": phone,
            "email": email
        }
        # 调用服务层方法，更新用户信息
        result = MpUserService_instance.update(id=userId,data=updateuser)
        if result["success"] is False:
            return ResponseUtil.error(data={"message": "更新失败"})

        return ResponseUtil.success(data={"message": "更新成功"})

@router.post("/getUserINFO")
def getUserINFO(userId:int = Body(...)):
        logger.info(f'/mp/user/getUserINFO, userId = {userId}')
        # 调用服务层方法，查询用户信息
        result = MpUserService_instance.get_one_by_filters(filters={"id": userId})
        # 若result为空，则返回空字典。不为空则返回result
        return ResponseUtil.success(data=result if result is not None else {})
