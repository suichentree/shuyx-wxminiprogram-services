from .base_service import BaseService
from ..dao.mp_user_exam_dao import MpUserExamDao
from ..model.mp_user_exam_model import MpUserExamModel

class MpUserExamService(BaseService[MpUserExamModel]):
    def __init__(self):
        """
        初始化服务实例
        创建DAO实例并传递给基类
        """
        dao_instance = MpUserExamDao()
        super().__init__(dao_instance)

    # 可以根据业务需求添加自定义方法

