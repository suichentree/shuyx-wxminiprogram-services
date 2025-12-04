from typing import Generic, TypeVar, List, Optional, Dict, Any, Type
from sqlalchemy.ext.declarative import DeclarativeMeta

# 定义模型类型变量
ModelType = TypeVar('ModelType', bound=DeclarativeMeta)

class BaseService(Generic[ModelType]):
    """
    通用服务基类
    提供CRUD操作的通用实现，作为DAO层和Controller层的中间层
    各层之间直接传递ModelType数据，不进行类型转换
    """

    def __init__(self, dao_instance):
        """
        初始化服务实例
        Args:
            dao_instance: DAO实例，处理数据库操作
        """
        self.dao = dao_instance

    def get_page_list(self, page_num: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        获取分页数据
        Args:
            page_num: 页码，默认1
            page_size: 每页大小，默认10
        """
        # 调用DAO层获取数据（已序列化）
        items = self.dao.get_page_list(page_size, page_num)
        total = self.dao.get_total()

        # 返回结果
        return {
            "data": items,
            "total": total,
            "page_num": page_num,
            "page_size": page_size
        }

    def get_by_id(self, id: int) -> Dict[str, Any]:
        """
        根据ID获取详情

        Args:
            id: 记录ID

        Returns:
            Optional[Dict[str, Any]]: 找到则返回序列化数据，未找到则返回None
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

        Args:
            filters: 查询条件字典

        Returns:
            Optional[Dict[str, Any]]: 找到的序列化数据，未找到则返回None
        """
        return self.dao.get_one_by_filters(filters)


    def add(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加记录到数据库
        Args:
            data: 要添加的数据字典
        """
        try:
            # 添加到数据库（返回序列化数据）
            new_item = self.dao.add(data)
            return {
                "success": True,
                "data": new_item if new_item else None,   # 返回新增记录的序列化数据
                "message": "添加成功"
            }
        except Exception as e:
            # 异常处理
            return {
                "success": False,
                "data": None,
                "message": f"添加失败,异常信息为：{str(e)}"
            }

    def update(self, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新记录

        Args:
            id: 记录ID
            data: 要更新的数据字典

        Returns:
            Dict[str, Any]: 更新结果
        """
        # 检查记录是否存在
        existing_item = self.dao.get_by_id(id)
        if not existing_item:
            return {"success": False, "data": None, "message": "记录不存在"}

        try:
            # 更新记录（返回是否成功）
            success = self.dao.update_by_id(id, data)
            return {
                "success": success,
                "data": None,
                "message": "更新成功" if success else "更新失败"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"更新失败,异常信息为：{str(e)}"
            }

    def delete(self, id: int) -> Dict[str, Any]:
        """
        删除记录

        Args:
            id: 记录ID

        Returns:
            Dict[str, Any]: 删除结果
        """
        # 检查记录是否存在
        existing_item = self.dao.get_by_id(id)
        if not existing_item:
            return {"success": False, "data": None, "message": "记录不存在"}

        try:
            # 执行删除（返回是否成功）
            success = self.dao.delete_by_id(id)
            return {
                "success": success,
                "data": None,
                "message": "删除成功" if success else "删除失败"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"删除失败: {str(e)}"
            }

