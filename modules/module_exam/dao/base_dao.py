from typing import List, Optional, Generic, TypeVar, Type, Dict, Any
from sqlalchemy.ext.declarative import DeclarativeMeta

# 导入数据库会话工厂
from config.database_config import session_maker

# 定义模型类型变量
ModelType = TypeVar("ModelType", bound=DeclarativeMeta)

class BaseDao(Generic[ModelType]):
    """
    基础数据访问对象类
    提供通用的CRUD操作，专注于数据访问层，不包含业务逻辑、日志和异常处理
    """

    def __init__(self, model: Type[ModelType]):
        """
        初始化数据访问对象
            model: SQLAlchemy模型类
        """
        self.model = model

    def get_page_list(self, page_size: int, page_num: int) -> List[ModelType]:
        """
        获取分页列表
            page_size: 每页大小
            page_num: 页码
        """
        with session_maker() as db_session:
            offset_value = (page_num - 1) * page_size
            record = db_session.query(self.model).offset(offset_value).limit(page_size).all()
            # 使用 SQLAlchemy-Serializer 序列化数据
            result = [item.to_dict() for item in record]
            # 返回序列化后的列表数据
            return result

    def get_total(self) -> int:
        """
        获取记录总数
        """
        with session_maker() as db_session:
            return db_session.query(self.model).count()

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        根据ID获取单条记录
            id: 记录ID
        """
        with session_maker() as db_session:
            record = db_session.query(self.model).filter(self.model.id == id).first()
            # 使用 SQLAlchemy-Serializer 序列化数据
            result = record.to_dict() if record else None
            return result

    def get_list_by_filters(self, filters: Optional[Dict[str, Any]] = None) -> List[ModelType]:
        """
        根据条件查询列表
            filters: 查询条件字典
        """
        with session_maker() as db_session:
            query = db_session.query(self.model)

            # 动态构建查询条件
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field) and value is not None:
                        query = query.filter(getattr(self.model, field) == value)

            record = query.all()
            # 使用 SQLAlchemy-Serializer 序列化数据
            result = record.to_dict() if record else None
            return result

    def update_by_id(self, id: int, data: Dict[str, Any]) -> bool:
        """
        根据ID更新信息
            id: 要更新的记录ID
            data: 更新数据字典
        """
        with session_maker() as db_session:
            # 检查记录是否存在
            existing = db_session.query(self.model).filter(self.model.id == id).first()
            if not existing:
                return False

            # 过滤出模型中存在的字段
            model_fields = {col.name for col in self.model.__table__.columns}
            update_data = {k: v for k, v in data.items() if k in model_fields and v is not None}

            if not update_data:
                return True  # 没有需要更新的字段，视为成功

            affected_rows = db_session.query(self.model).filter(self.model.id == id).update(update_data)
            db_session.commit()  # 显式提交事务
            return affected_rows > 0

    def delete_by_id(self, id: int) -> bool:
        """
        根据ID删除记录
            id: 要删除的记录ID
        """
        with session_maker() as db_session:
            # 检查记录是否存在
            existing = db_session.query(self.model).filter(self.model.id == id).first()
            if not existing:
                return False

            affected_rows = db_session.query(self.model).filter(self.model.id == id).delete()
            db_session.commit()  # 显式提交事务
            return affected_rows > 0

    def add(self, data: Dict[str, Any]) -> Optional[ModelType]:
        """
        添加新记录
            data: 添加数据字典
        """
        with session_maker() as db_session:
            # 过滤出模型中存在的字段
            model_fields = {col.name for col in self.model.__table__.columns}
            model_data = {k: v for k, v in data.items() if k in model_fields}

            instance = self.model(**model_data)
            db_session.add(instance)
            db_session.flush()  # 获取新生成的ID
            db_session.commit()  # 显式提交事务
            # 返回序列化后的数据
            return instance.to_dict()

    def get_one_by_filters(self, filters: Dict[str, Any]) -> Optional[ModelType]:
        """
        根据条件获取单条记录
            filters: 查询条件字典
        """
        with session_maker() as db_session:
            query = db_session.query(self.model)

            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.filter(getattr(self.model, field) == value)

            # 执行查询并获取第一条记录
            record = query.first()
            # 使用 SQLAlchemy-Serializer 序列化数据
            result = record.to_dict() if record else None
            # 返回序列化后的数据
            return result