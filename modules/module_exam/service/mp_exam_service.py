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
        dao_instance = MpExamDao()
        super().__init__(dao_instance)

    # 可以根据业务需求添加自定义方法
