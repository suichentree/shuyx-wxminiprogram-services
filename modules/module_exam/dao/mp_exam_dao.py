from modules.module_exam.model.mp_exam_model import MpExamModel
from .base_dao import BaseDao
from modules.module_exam.dto.mp_exam_dto import MpExamDTO

# 继承基础Dao类，可添加自定义方法
# 注：专注于数据访问操作，异常直接抛出给service层处理
class MpExamDao(BaseDao[MpExamModel, MpExamDTO]):
    def __init__(self):
        """初始化实例"""
        super().__init__(MpExamModel, MpExamDTO)

    # 可以根据业务需求添加自定义方法
