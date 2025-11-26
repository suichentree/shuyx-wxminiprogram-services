from .base_service import BaseService
from ..dao.mp_user_dao import MpUserDao
from ..model.mp_user_model import MpUserModel

class MpUserService(BaseService[MpUserModel]):
    def __init__(self):
        """
        初始化服务实例
        创建DAO实例并传递给基类
        """
        dao_instance = MpUserDao()
        super().__init__(dao_instance)

    # 可以根据业务需求添加自定义方法

