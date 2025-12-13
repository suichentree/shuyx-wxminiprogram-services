from .base_service import BaseService
from ..dao.mp_option_dao import MpOptionDao
from ..dto.mp_option_dto import MpOptionDTO
from ..model.mp_option_model import MpOptionModel


class MpOptionService(BaseService[MpOptionModel, MpOptionDTO]):
    def __init__(self):
        """
        初始化服务实例
        创建DAO实例并传递给基类
        """
        dao_instance = MpOptionDao()
        super().__init__(dao_instance)

    # 可以根据业务需求添加自定义方法

