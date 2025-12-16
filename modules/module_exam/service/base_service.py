from typing import Generic, TypeVar, List, Optional, Dict, Any, Type, Callable

from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta

# 定义泛型
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


    def get_page_list_by_filters(self, page_num: int = 1, page_size: int = 10, filters: DtoType = None,sort_by: List[str] = None) -> List[DtoType]:
        """
        获取分页数据（DTO形式）
            page_num: 页码，默认1
            page_size: 每页大小，默认10
            filters: 查询条件DTO
        """
        # 调用DAO层获取数据（已转换为DTO）并返回
        return self.dao.get_page_list_by_filters(page_size, page_num, filters,sort_by)

    def get_page_list_by_filters_as_dict(self, page_num: int = 1, page_size: int = 10, filters: dict = None,sort_by: List[str] = None) -> List[DtoType]:
        """
        获取分页数据(dict形式)
            page_num: 页码，默认1
            page_size: 每页大小，默认10
            filters: 查询条件dict
        """
        return self.dao.get_page_list_by_filters_as_dict(page_size, page_num, filters, sort_by)


    def get_total_by_filters(self,filters: DtoType = None) -> int:
        """
        获取符合条件的记录总数（DTO形式）
            filters: 查询条件DTO
        """
        return self.dao.get_total_by_filters(filters)

    def get_by_id(self, id: int) -> DtoType:
        """
        根据ID获取详情
            id: 记录ID
        """
        return self.dao.get_by_id(id)

    def get_list_by_filters(self, filters: DtoType = None,sort_by: List[str] = None) -> List[DtoType]:
        """
        根据条件获取列表（DTO形式）
            filters: 查询条件DTO
        """
        return self.dao.get_list_by_filters(filters,sort_by)

    def get_one_by_filters(self, filters: DtoType = None) -> DtoType:
        """
        根据条件获取单条记录
            filters: 查询条件DTO
        """
        return self.dao.get_one_by_filters(filters)

    def add(self, data: DtoType) -> DtoType:
        """
        添加记录到数据库（DTO形式）
            data: 要添加的数据DTO
        """
        return self.dao.add(data)

    def update_by_id(self, id: int, update_data: DtoType) -> bool:
        """
        更新记录（返回是否成功）（DTO形式）
            id: 记录ID
            update_data: 要更新的数据DTO
        """
        return self.dao.update_by_id(id, update_data)

    def delete_by_id(self, id: int) -> bool:
        """
        删除记录
            id: 记录ID
        """
        return self.dao.delete_by_id(id)

    def execute_raw_sql(self, sql: str, params: Dict = None) -> bool:
        """
        执行原生SQL语句（适用于INSERT、UPDATE、DELETE等）
            sql: 原生SQL语句
            params: SQL参数（可选）
            返回：是否执行成功

        调用示例
        sql = "INSERT INTO users (name, age) VALUES (:name, :age)"
        params = {"name": "张三", "age": 30}
        affected_rows = execute_raw_sql(sql, params)
        """
        return self.dao.execute_raw_sql(sql, params)

    def query_raw_sql(self, sql: str, params: Dict = None) -> Any:
        """
        执行原生SQL查询并返回查询结果
            sql: 原生SQL语句
            params: SQL参数（可选）

        调用示例
        sql = "SELECT * FROM users WHERE age > :age"
        params = {"age": 18}
        results = query_raw_sql(sql, params)
        """
        return self.dao.query_raw_sql(sql, params)


    def session_execute_query(self, query_func) -> Any:
        """
        session_execute_query方法用于执行自定义查询操作，可以直接使用sqlalchemy的原生查询方法
        参数:
            query_func: 接收lambda匿名函数。该函数内部使用db_session进行查询操作。
        返回:
            查询结果

        调用示例
        def get_all():
            return session_execute_query(lambda db_session: db_session.query(self.model).all())
        """
        return self.dao.session_execute_query(query_func)