from typing import List, Optional

from .base_service import BaseService
from ..dao.mp_user_exam_dao import MpUserExamDao
from ..dto.mp_user_exam_dto import MpUserExamDTO
from ..model.mp_user_exam_model import MpUserExamModel

class MpUserExamService(BaseService[MpUserExamModel, MpUserExamDTO]):
    def __init__(self):
        """
        初始化服务实例
        创建DAO实例并传递给基类
        """
        self.dao_instance = MpUserExamDao()
        super().__init__(self.dao_instance)

    # 可以根据业务需求添加自定义方法

    def get_last_user_exam(self, userId: int, exam_id: int) -> Optional[MpUserExamDTO]:
        # 根据exam_id 查询对应的测试信息
        # 排序按id降序，取最近一次的测试记录
        mp_user_exams_list: List[MpUserExamDTO] = self.dao_instance.get_list_by_filters(filters=MpUserExamDTO(
            user_id=userId,
            exam_id=exam_id,
        ), sort_by=['-id'])
        # 若用户有做过该测试，则取最近一次的测试记录
        if len(mp_user_exams_list) > 0:
            return mp_user_exams_list[0]
        else:
            return None


