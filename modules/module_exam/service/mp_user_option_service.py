from .base_service import BaseService
from ..dao.mp_user_option_dao import MpUserOptionDao
from ..model.mp_user_option_model import MpUserOptionModel

from ..dto.mp_user_option_dto import MpUserOptionDTO

class MpUserOptionService(BaseService[MpUserOptionModel, MpUserOptionDTO]):
    def __init__(self):
        """
        初始化服务实例
        创建DAO实例并传递给基类
        """
        dao_instance = MpUserOptionDao()
        super().__init__(dao_instance)

    # 可以根据业务需求添加自定义方法

