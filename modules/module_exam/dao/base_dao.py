from typing import List, Optional, Generic, TypeVar, Type, Dict, Any, Callable
from pydantic import BaseModel
from sqlalchemy import asc, desc, text
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

# 导入数据库会话工厂
from config.database_config import session_maker

# 定义泛型
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
DtoType = TypeVar("DtoType", bound=BaseModel)

class BaseDao(Generic[ModelType, DtoType]):
    """
    基础数据访问对象类
    提供通用的CRUD操作，专注于数据访问层，不包含业务逻辑、日志和异常处理

    其中session_execute_query方法用于执行自定义的高级查询操作，可以直接使用sqlalchemy的内置方法进行查询
    """
    def __init__(self, model: Type[ModelType], dto: Type[DtoType]):
        """
        初始化数据访问对象
            model: SQLAlchemy 模型类
            dto: Pydantic 模型类
        """
        self.model = model
        self.dto = dto

    def _model_to_dict__(self, model: ModelType) -> Dict[str, Any]:
        """
        将SQLAlchemy模型实例转换为字典，自动将SQLAlchemy模型实例中datetime类型的字段转换为字符串
        """
        model_dict = {}
        for column in model.__table__.columns:
            value = getattr(model, column.name)
            # 检查是否为datetime类型
            if isinstance(value, datetime):
                # 将datetime类型的字段转换为字符串
                model_dict[column.name] = value.isoformat()
            else:
                # 其他类型直接赋值
                model_dict[column.name] = value
        return model_dict

    def __dto_to_model__(self, dto: DtoType) -> ModelType:
        """
        将Pydantic模型实例 转换为 SQLAlchemy模型实例
            输入: Pydantic 模型实例
            输出: SQLAlchemy 模型实例
        """
        # 先将DTO转换为字典，过滤出非None值的字段
        model_data = dto.model_dump(exclude_unset=True, exclude_none=True)
        # 然后查询出SQLAlchemy模型的字段
        model_fields = {col.name for col in self.model.__table__.columns}
        # 根据SQLAlchemy模型字段，过滤出DTO中存在的字段
        model_data = {k: v for k, v in model_data.items() if k in model_fields}
        # 开始转换
        return self.model(**model_data)

    def __model_to_dto__(self, model: ModelType) -> DtoType:
        """
        将SQLAlchemy模型实例 转换为 Pydantic模型实例
            输入: SQLAlchemy 模型实例
            输出: Pydantic 模型实例
        """
        # 先将SQLAlchemy模型实例转换为字典
        model_dict = self._model_to_dict__(model)
        # 然后使用model_validate方法将字典转换为Pydantic模型实例
        return self.dto.model_validate(model_dict)


    def get_page_list_by_filters(self, page_size: int, page_num: int, filters: DtoType = None, sort_by: List[str] = None) -> List[DtoType]:
        """
        获取分页列表
            page_size: 每页大小
            page_num: 页码
            filters: 查询条件DTO。例如 XXXDTO(field1=value1, field2=value2)
            sort_by: 排序字段，是一个字符串列表。例如 ["field1", "-field2"] 表示按field1升序，按field2降序排序。
        """
        with session_maker() as db_session:
            query = db_session.query(self.model)

            # 动态构建查询条件
            if filters:
                # 将DTO转换为字典，过滤出非None值的字段
                filters_dict = filters.model_dump(exclude_unset=True, exclude_none=True)
                for field, value in filters_dict.items():
                    if hasattr(self.model, field) and value is not None:
                            query = query.filter(getattr(self.model, field) == value)

            # 动态构建排序条件
            if sort_by:
                # 遍历排序字段列表
                for sort_field in sort_by:
                    # 判断排序方向
                    if sort_field.startswith('-'):
                        # 降序
                        field_name = sort_field[1:]
                        if hasattr(self.model, field_name):
                            query = query.order_by(desc(getattr(self.model, field_name)))
                    else:
                        # 升序
                        if hasattr(self.model, sort_field):
                            query = query.order_by(asc(getattr(self.model, sort_field)))

            # 计算分页偏移量
            offset_value = (page_num - 1) * page_size
            # 获取当前分页数据
            records = query.offset(offset_value).limit(page_size).all()
            # 通过__model_to_dto__方法将sqlAlchemy模型实例转换为DTO实例,并返回
            return [self.__model_to_dto__(record) for record in records]


    def get_page_list_by_filters_as_dict(self, page_size: int, page_num: int, filters: Dict = None, sort_by: List[str] = None) -> List[DtoType]:
        """
        获取分页列表（dict形式）
            page_size: 每页大小
            page_num: 页码
            filters: 查询条件字典。例如 {"filed1": value1, "filed2": value2}
            sort_by: 排序字段，是一个字符串列表。例如 ["field1", "-field2"] 表示按field1升序，按field2降序排序。
        """
        with session_maker() as db_session:
            query = db_session.query(self.model)

            # 动态构建查询条件
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field) and value is not None:
                            query = query.filter(getattr(self.model, field) == value)

            # 动态构建排序条件
            if sort_by:
                # 遍历排序字段列表
                for sort_field in sort_by:
                    # 判断排序方向
                    if sort_field.startswith('-'):
                        # 降序
                        field_name = sort_field[1:]
                        if hasattr(self.model, field_name):
                            query = query.order_by(desc(getattr(self.model, field_name)))
                    else:
                        # 升序
                        if hasattr(self.model, sort_field):
                            query = query.order_by(asc(getattr(self.model, sort_field)))

            # 计算分页偏移量
            offset_value = (page_num - 1) * page_size
            # 获取当前分页数据
            records = query.offset(offset_value).limit(page_size).all()
            # 通过__model_to_dto__方法将sqlAlchemy模型实例转换为DTO实例,并返回
            return [self.__model_to_dto__(record) for record in records]


    def get_total_by_filters(self, filters: DtoType = None) -> int:
        """
        获取记录总数（dto形式）
            filters: 查询条件DTO。例如 XXXDTO(filed1=value1, filed2=value2)
        """
        with session_maker() as db_session:
            query = db_session.query(self.model)

            # 动态构建查询条件
            if filters:
                # 将DTO转换为字典，过滤出非None值的字段
                filters_dict = filters.model_dump(exclude_unset=True, exclude_none=True)
                for field, value in filters_dict.items():
                    if hasattr(self.model, field) and value is not None:
                            query = query.filter(getattr(self.model, field) == value)

            return query.count()

    def get_by_id(self, id: int) -> DtoType:
        """
        根据ID获取单条记录
            id: 记录ID
        """
        with session_maker() as db_session:
            # 查询单条记录
            record = db_session.query(self.model).filter(self.model.id == id).first()
            # 通过__model_to_dto__方法将sqlAlchemy模型实例转换为DTO实例,并返回DTO数据
            return self.__model_to_dto__(record) if record else None

    def get_list_by_filters(self, filters: DtoType = None,sort_by: List[str] = None) -> List[DtoType]:
        """
        根据条件查询列表（dto形式）
            filters: 查询条件DTO，内部会将其转换为字典形式。例如 XXXDTO(filed1=value1, filed2=value2)
            sort_by: 排序字段，是一个字符串列表。例如 ["field1", "-field2"] 表示按field1升序，按field2降序排序。
        """
        with session_maker() as db_session:
            query = db_session.query(self.model)

            # 动态构建查询条件
            if filters:
                # 将DTO转换为字典，过滤出非None值的字段
                filters_dict = filters.model_dump(exclude_unset=True, exclude_none=True)
                for field, value in filters_dict.items():
                    if hasattr(self.model, field) and value is not None:
                            query = query.filter(getattr(self.model, field) == value)

            # 动态构建排序条件
            if sort_by:
                # 遍历排序字段列表
                for sort_field in sort_by:
                    # 判断排序方向
                    if sort_field.startswith('-'):
                        # 降序
                        field_name = sort_field[1:]
                        if hasattr(self.model, field_name):
                            query = query.order_by(desc(getattr(self.model, field_name)))
                    else:
                        # 升序
                        if hasattr(self.model, sort_field):
                            query = query.order_by(asc(getattr(self.model, sort_field)))

            # 执行查询并获取所有记录
            records = query.all()
            # 通过__model_to_dto__方法将sqlAlchemy模型实例转换为DTO实例,并返回DTO列表数据
            return [self.__model_to_dto__(record) for record in records]

    def get_one_by_filters(self, filters: DtoType = None) -> DtoType:
        """
        根据条件获取单条记录（dto形式）
            filters: 查询条件DTO，内部会将其转换为字典形式，然后再根据字典构建查询条件。
            例如 XXXDTO(field1=value1, field2=value2)
        """
        with session_maker() as db_session:
            query = db_session.query(self.model)

            # 动态构建查询条件
            if filters:
                # 将DTO转换为字典，过滤出非None值的字段
                filters_dict = filters.model_dump(exclude_unset=True, exclude_none=True)
                for field, value in filters_dict.items():
                    if hasattr(self.model, field) and value is not None:
                            query = query.filter(getattr(self.model, field) == value)

            # 执行查询并获取第一条记录
            record = query.first()
            # 通过__model_to_dto__方法将sqlAlchemy模型实例转换为DTO实例,并返回DTO数据
            return self.__model_to_dto__(record) if record else None


    def update_by_id(self, id: int, update_data: DtoType) -> bool:
        """
        根据ID更新信息（dto形式）
            id: 要更新的记录ID
            update_date: 更新数据DTO
        """
        with session_maker() as db_session:
            # 先获取model模型类的所有字段名
            # 然后将DTO转换为字典，过滤出model模型类中存在的字段
            model_fields = {col.name for col in self.model.__table__.columns}
            update_data_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            new_update_data = {k: v for k, v in update_data_dict.items() if k in model_fields}

            if not new_update_data:
                return True  # 没有需要更新的字段，视为成功

            # 执行更新并获取受影响的行数
            affected_rows = db_session.query(self.model).filter(self.model.id == id).update(new_update_data)
            db_session.commit()  # 显式提交事务
            return affected_rows > 0

    def delete_by_id(self, id: int) -> bool:
        """
        根据ID删除记录
            id: 要删除的记录ID
        """
        with session_maker() as db_session:
            # 执行删除并获取受影响的行数
            # 如果受影响的行数为0，说明记录不存在。大于0说明删除成功
            affected_rows = db_session.query(self.model).filter(self.model.id == id).delete()
            db_session.commit()  # 显式提交事务
            return affected_rows > 0

    def add(self, data: DtoType=None) -> DtoType:
        """
        添加新记录(DTO形式)
            data: 添加数据DTO
        """
        if data is None:
            return None

        with session_maker() as db_session:
            # 遍历data，过滤出模型中存在的字段
            model_fields = {col.name for col in self.model.__table__.columns}
            model_data = data.model_dump(exclude_unset=True, exclude_none=True)
            model_data = {k: v for k, v in model_data.items() if k in model_fields}

            # 将字典数据转换为模型实例
            instance = self.model(**model_data)
            db_session.add(instance)
            db_session.commit()  # 显式提交事务
            # 将sqlAlchemy模型实例转换为DTO返回，会返回包含ID的完整DTO数据
            return self.__model_to_dto__(instance)


    def session_execute_query(self, query_func):
        """
        session_execute_query方法用于执行自定义的高级查询操作，可以直接使用sqlalchemy的内置方法进行查询
        参数:
            query_func: 接收db_session的查询函数
        返回:
            查询结果

        调用示例
        def get_all():
            return session_execute_query(lambda db_session: db_session.query(self.model).all())
        """
        with session_maker() as db_session:
            try:
                result = query_func(db_session)
                # 当为查询操作时，此处不会有变更需要提交。其他操作时需要显式调用commit()方法提交事务
                # 这里只是为了符合事务的完整性，避免后续操作受到影响
                db_session.commit()

                print(result)

                # 处理JOIN查询结果（包含多个模型实例的元组）
                if isinstance(result, list) and result and isinstance(result[0], tuple):
                    return result  # 直接返回原始结果，由调用方处理

                # 转换为DTO
                # 处理列表类型结果
                if isinstance(result, list):
                    return [self.__model_to_dto__(record) for record in result]
                # 处理单个模型实例
                elif isinstance(result, self.model):
                    return self.__model_to_dto__(result) if result else None
            except Exception as e:
                db_session.rollback()
                raise