from typing import List
from modules.module_exam.model.mp_exam_model import MpExamModel
from .base_dao import BaseDao
from config.database_config import session_maker


# 考试数据访问类，继承基础Dao类，添加特定于考试模型的自定义方法
# 注：专注于数据访问操作，异常直接抛出给service层处理
class MpExamDao(BaseDao[MpExamModel]):
    def __init__(self):
        """初始化考试DAO实例"""
        super().__init__(MpExamModel)

    # 可以根据业务需求添加自定义方法

    def get_exams_by_type(self, exam_type: str) -> List[MpExamModel]:
        """根据考试类型获取考试列表
        Args:
            exam_type: 考试类型
        Returns:
            List[MpExamModel]: 符合类型的考试列表
        """

        with session_maker() as db_session:
            return db_session.query(MpExamModel).filter(MpExamModel.type == exam_type).all()

    def get_active_exams(self) -> List[MpExamModel]:
        """获取未禁用的考试列表
        Returns:
            List[MpExamModel]: 未禁用的考试列表
        """
        with session_maker() as db_session:
            return db_session.query(MpExamModel).filter(MpExamModel.isBan == 0).all()