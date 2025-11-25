from typing import List, Dict, Any
from ..dao.mp_exam_dao import MpExamDao
from ..model.mp_exam_model import MpExamModel
from .base_service import BaseService

class MpExamService(BaseService[MpExamModel]):
    """
    考试服务类，继承自通用服务基类
    提供考试相关的业务逻辑处理
    """

    def __init__(self):
        """
        初始化考试服务实例
        创建DAO实例并传递给基类
        """
        dao_instance = MpExamDao()
        super().__init__(dao_instance)

    def add_exam(self, data) -> Dict[str, Any]:
        """
        添加考试（带业务逻辑校验）

        Args:
            data: 考试数据

        Returns:
            Dict[str, Any]: 添加结果

        Raises:
            ValueError: 当参数校验失败时
        """
        # 业务逻辑校验
        if not data.name or not data.type:
            raise ValueError("考试名称和类型不能为空")

        # 调用父类的添加方法
        return super().add(data)

    def update_exam(self, data) -> Dict[str, Any]:
        """
        更新考试信息

        Args:
            data: 包含更新信息的数据

        Returns:
            Dict[str, Any]: 更新结果

        Raises:
            ValueError: 当参数校验失败时
        """
        if not data.id:
            raise ValueError("更新操作必须提供ID")

        # 调用父类的更新方法
        return super().update(data.id, data)

    def delete_exam(self, id: int) -> Dict[str, Any]:
        """
        删除考试

        Args:
            id: 要删除的考试ID

        Returns:
            Dict[str, Any]: 删除结果
        """
        # 调用父类的删除方法
        return super().delete(id)

    def get_exams_by_type(self, exam_type: str) -> List[MpExamModel]:
        """
        根据类型获取考试列表（特定业务方法）

        Args:
            exam_type: 考试类型

        Returns:
            List[MpExamModel]: 符合类型的考试模型列表
        """
        # 直接调用DAO层的特定方法，不进行DTO转换
        return self.dao.get_exams_by_type(exam_type)

    def get_active_exams(self) -> List[MpExamModel]:
        """
        获取未禁用的考试列表（特定业务方法）

        Returns:
            List[MpExamModel]: 未禁用的考试模型列表
        """
        # 直接调用DAO层的特定方法，不进行DTO转换
        return self.dao.get_active_exams()