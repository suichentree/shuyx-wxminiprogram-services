from modules.module_exam.model.mp_user_exam_model import MpUserExamModel
from .base_dao import BaseDao
from ..dto.mp_user_exam_dto import MpUserExamDTO
# 导入数据库会话工厂
from config.database_config import session_maker

# 继承基础Dao类，可添加自定义方法
# 注：专注于数据访问操作，异常直接抛出给service层处理
class MpUserExamDao(BaseDao[MpUserExamModel,MpUserExamDTO]):
    def __init__(self):
        """初始化DAO实例"""
        super().__init__(MpUserExamModel,MpUserExamDTO)

    # 可以根据业务需求添加自定义方法

    def findLastOneByIsFinish(self):
        with session_maker() as session:
            mp_user_exam = session.query(self.model).filter(self.model.is_finish == True).order_by(desc(self.model.id)).first()
            return mp_user_exam

