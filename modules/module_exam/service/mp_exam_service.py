from typing import List

from ..dao.mp_exam_dao import MpExamDao
from ..dto.mp_exam_dto import MpExamDTO
from ..model.mp_exam_model import MpExamModel
from .base_service import BaseService

class MpExamService(BaseService[MpExamModel,MpExamDTO]):
    """
    MpExamService 类，继承自通用服务基类
    提供相关的业务逻辑处理
    """

    def __init__(self):
        """
        初始化考试服务实例
        创建DAO实例并传递给基类
        """
        self.dao_instance = MpExamDao()
        super().__init__(self.dao_instance)

    # 可以根据业务需求添加自定义方法

    def get_all_exam_id(self) -> List[int]:
        """
        查询所有考试的id，返回一个包含所有考试id的列表
        """
        examlist:List[MpExamDTO] = self.dao_instance.get_list_by_filters(filters=None)
        examids:List[int] = []
        for exam in examlist:
            examids.append(exam.id)
        return examids
