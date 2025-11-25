from modules.module_exam.model.mp_user_option_model import MpUserOptionModel
from .base_dao import BaseDao

# 继承基础Dao类，可添加自定义方法
# 注：专注于数据访问操作，异常直接抛出给service层处理
class MpUserOptionDao(BaseDao[MpUserOptionModel]):
    def __init__(self):
        """初始化DAO实例"""
        super().__init__(MpUserOptionModel)

    # 可以根据业务需求添加自定义方法
