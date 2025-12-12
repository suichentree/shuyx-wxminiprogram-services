from typing import Generic, TypeVar, List, Optional, Dict, Any, Type

from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta

# 定义模型类型变量
ModelType = TypeVar('ModelType', bound=DeclarativeMeta)
DtoType = TypeVar('DtoType', bound=BaseModel)

class BaseService(Generic[ModelType, DtoType]):
    """
    通用服务基类 提供CRUD操作的通用实现，作为DAO层和Controller层的中间层
    各层之间使用DTO数据进行交互，实现强类型检查
    """

    def __init__(self, dao_instance):
        """
        初始化服务实例
            dao_instance: DAO实例，处理数据库操作
        """
        self.dao = dao_instance

    def get_page_list_by_filters(self, page_num: int = 1, page_size: int = 10, filters: DtoType = None) -> DtoType:
        """
        获取分页数据
            page_num: 页码，默认1
            page_size: 每页大小，默认10
            filters: 查询条件DTO
        """
        # 调用DAO层获取数据（已转换为DTO）并返回
        return self.dao.get_page_list_by_filters(page_size, page_num, filters)

    def get_total(self,filters: DtoType = None) -> int:
        """
        获取符合条件的记录总数
            filters: 查询条件DTO
        """
        return self.dao.get_total_by_filters(filters)

    def get_by_id(self, id: int) -> DtoType:
        """
        根据ID获取详情
            id: 记录ID
        """
        return self.dao.get_by_id(id)

    def get_list_by_filters(self, filters: DtoType = None) -> List[DtoType]:
        """
        根据条件获取列表
            filters: 查询条件DTO
        """
        return self.dao.get_list_by_filters(filters)

    def get_one_by_filters(self, filters: DtoType) -> DtoType:
        """
        根据条件获取单条记录
            filters: 查询条件DTO
        """
        return self.dao.get_one_by_filters(filters)

    def add(self, data: DtoType) -> DtoType:
        """
        添加记录到数据库
            data: 要添加的数据DTO
        """
        return self.dao.add(data)

    def update_by_id(self, id: int, data: DtoType) -> bool:
        """
        更新记录（返回是否成功）
            id: 记录ID
            data: 要更新的数据DTO
        """
        return self.dao.update_by_id(id, data)

    def delete_by_id(self, id: int) -> bool:
        """
        删除记录
            id: 记录ID
        """
        return self.dao.delete_by_id(id)

