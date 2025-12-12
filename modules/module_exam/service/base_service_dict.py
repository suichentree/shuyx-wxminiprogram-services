from typing import Generic, TypeVar, List, Optional, Dict, Any, Type
from sqlalchemy.ext.declarative import DeclarativeMeta

# 定义模型类型变量
ModelType = TypeVar('ModelType', bound=DeclarativeMeta)

class BaseServiceDict(Generic[ModelType]):
    """
    通用服务基类 BaseServiceDict 提供CRUD操作的通用实现，作为DAO层和Controller层的中间层
    BaseServiceDict类的各个主要方法都是接收字典类型的参数，而不是模型实例。
    """

    def __init__(self, dao_instance):
        """
        初始化服务实例
        Args:
            dao_instance: DAO实例，处理数据库操作
        """
        self.dao = dao_instance

    def get_page_list(self, page_num: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        获取分页数据
        Args:
            page_num: 页码，默认1
            page_size: 每页大小，默认10
        """
        # 调用DAO层获取数据（已序列化）
        items = self.dao.get_page_list_by_filters(page_size, page_num, filters)
        total = self.dao.get_total_by_filters(filters)
        # 返回结果
        return {
            "data": items,
            "total": total,
            "page_num": page_num,
            "page_size": page_size
        }

    def get_total(self,filters: Optional[Dict[str, Any]] = None) -> int:
        """
        获取符合条件的记录总数
        Args:
            filters: 查询条件字典
        """
        return self.dao.get_total_by_filters(filters)

    def get_by_id(self, id: int) -> Dict[str, Any]:
        """
        根据ID获取详情
            id: 记录ID
        """
        return self.dao.get_by_id(id)

    def get_list_by_filters(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        根据条件获取列表

        Args:
            filters: 查询条件字典

        Returns:
            List[Dict[str, Any]]: 符合条件的序列化数据列表
        """
        return self.dao.get_list_by_filters(filters)

    def get_one_by_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据条件获取单条记录
            filters: 查询条件字典
        """
        return self.dao.get_one_by_filters(filters)

    def add(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加记录到数据库
        Args:
            data: 要添加的数据字典
        """
        return self.dao.add(data)

    def update_by_id(self, id: int, data: Dict[str, Any]) -> bool:
        """
        更新记录（返回是否成功）
            id: 记录ID
            data: 要更新的数据字典
        """
        return self.dao.update_by_id(id, data)

    def delete_by_id(self, id: int) -> bool:
        """
        删除记录
            id: 记录ID
        """
        return self.dao.delete_by_id(id)

