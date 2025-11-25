from modules.module_exam.model.mp_user_model import MpUserModel
from .base_dao import BaseDao

# 继承基础Dao类，可添加自定义方法
# 注：专注于数据访问操作，异常直接抛出给service层处理
class MpUserDao(BaseDao[MpUserModel]):
    def __init__(self):
        """初始化DAO实例"""
        super().__init__(MpUserModel)

    # 可以根据业务需求添加自定义方法
