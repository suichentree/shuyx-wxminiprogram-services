from .base_service import BaseService
from ..dao.mp_question_dao import MpQuestionDao
from ..model.mp_question_model import MpQuestionModel


class MpQuestionService(BaseService[MpQuestionModel]):
    """
    服务类，继承自通用服务基类
    提供相关的业务逻辑处理
    """

    def __init__(self):
        """
        初始化服务实例
        创建DAO实例并传递给基类
        """
        dao_instance = MpQuestionDao()
        super().__init__(dao_instance)

    # 可以根据业务需求添加自定义方法

