from fastapi import APIRouter,Body
from config.log_config import logger
from modules.module_exam.service.mp_user_service import MpUserService
from modules.module_exam.model.mp_user_model import MpUserModel
from utils.response_util import ResponseUtil

# 创建路由实例
router = APIRouter(prefix='/mp/user', tags=['mp_user接口'])
# 创建服务实例
service = MpUserService()

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
    result = service.add(data=user)
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
    result: MpUserModel = service.get_one_by_filters(filters=user)
    print(result)
    if result is None:
        return ResponseUtil.error(data={"userId": 0, "isLogin": 0, "message": "电话登录失败"})

    return ResponseUtil.success(data={"userId": result["id"], "isLogin": 1, "message": "电话登录成功"})

"""
重置密码
"""
@router.post("/resetPass")
def phoneLogin(phone:str,password:str,newpassword:str):
    logger.info(f'/mp/user/resetPass, phone = {phone} password = {password}')
    # 构造用户字典数据
    user = {
        "phone": phone,
        "password": password
    }
    # 调用服务层方法，新增用户
    result = service.get_one_by_filters(filters=user)
    if result["success"]:
        # 构造新的用户字典数据
        newuser = {
            "id": result["data"].id,
            "password": newpassword
        }
        newresult = service.update(data=newuser)
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
def wxLogin(code:str,head:str,name:str,gender:str,address:str):
        logger.info(f'/mp/user/wxLogin, code = {code} head = {head} name = {name} gender = {gender} address = {address}')
        # 构造用户字典数据
        user = {
            "code": code,
            "head": head,
            "name": name,
            "gender": gender,
            "address": address
        }
        # 调用服务层方法，新增用户
        result = service.add(data=user)
        if result["success"]:
            return ResponseUtil.success(data={"isLogin": 1, "message": "微信登录成功"})
        else:
            return ResponseUtil.error(data={"isLogin": 0, "message": "微信登录失败"})
