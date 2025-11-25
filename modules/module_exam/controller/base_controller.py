from fastapi import APIRouter, Body
from typing import Generic, TypeVar, List, Dict, Any, Optional
from datetime import datetime
from config.log_config import logger
from utils.response_util import ResponseUtil
from sqlalchemy.ext.declarative import DeclarativeMeta

# 定义类型变量
ModelType = TypeVar('ModelType', bound=DeclarativeMeta)
ServiceType = TypeVar('ServiceType')


class BaseController(Generic[ModelType, ServiceType]):
    """
    基础控制器类
    提供通用的CRUD操作、错误处理和日志记录
    处理HTTP请求并调用服务层，负责模型到字典的转换
    """

    def __init__(self, service_class: type, model_class: type, prefix: str, tags: List[str]):
        """
        初始化基础控制器

        Args:
            service_class: 服务类
            model_class: 模型类
            prefix: 路由前缀
            tags: 路由标签
        """
        self.service_class = service_class
        self.model_class = model_class
        self.router = APIRouter(prefix=prefix, tags=tags)
        self._register_routes()

    def _register_routes(self):
        """
        注册基础路由
        子类可以重写此方法来注册额外的路由
        """
        pass

    def model_to_dict(self, model: ModelType) -> Dict[str, Any]:
        """
        将SQLAlchemy模型转换为字典

        Args:
            model: SQLAlchemy模型实例

        Returns:
            Dict[str, Any]: 转换后的字典
        """
        result = {}
        for column in model.__table__.columns:
            value = getattr(model, column.name)
            # 处理datetime类型
            if isinstance(value, datetime):
                result[column.name] = str(value)
            else:
                result[column.name] = value
        return result

    def models_to_dicts(self, models: List[ModelType]) -> List[Dict[str, Any]]:
        """
        将模型列表转换为字典列表

        Args:
            models: 模型实例列表

        Returns:
            List[Dict[str, Any]]: 字典列表
        """
        return [self.model_to_dict(model) for model in models]

    def _handle_exception(self, func_name: str, e: Exception, default_msg: str) -> Any:
        """
        统一异常处理

        Args:
            func_name: 函数名
            e: 异常对象
            default_msg: 默认错误消息

        Returns:
            Any: 错误响应字典
        """
        logger.exception(f"{func_name}失败: {str(e)}")
        return ResponseUtil.error(msg=f"{default_msg}: {str(e)}", as_dict=True)

    def _handle_value_error(self, func_name: str, e: ValueError, default_msg: str) -> Any:
        """
        处理值错误异常

        Args:
            func_name: 函数名
            e: 值错误异常对象
            default_msg: 默认错误消息

        Returns:
            Any: 失败响应字典
        """
        logger.warning(f"{func_name}参数校验失败: {str(e)}")
        return ResponseUtil.failure(msg=str(e), as_dict=True)

    # 基础CRUD方法，子类可以直接调用
    def get_page_list(self, page_num: int, page_size: int) -> Any:
        """
        分页获取列表
        """
        try:
            result = self.service_class().get_page_list(page_num=page_num, page_size=page_size)

            if result and 'data' in result:
                result['data'] = self.models_to_dicts(result['data'])

            return ResponseUtil.success(data=result['data'], dict_content={'total': result.get('total', 0)}, as_dict=True)
        except Exception as e:
            return self._handle_exception("获取列表", e, "获取列表失败")

    def get_by_id(self, item_id: int) -> Any:
        """
        根据ID获取详情
        """
        try:
            model = self.service_class().get_by_id(item_id)

            if not model:
                return ResponseUtil.failure(msg="数据不存在", as_dict=True)

            return ResponseUtil.success(data=self.model_to_dict(model), as_dict=True)
        except Exception as e:
            return self._handle_exception("获取详情", e, "获取详情失败")

    def add_item(self, item_data: dict) -> Any:
        """
        添加数据
        """
        try:
            result = self.service_class().add(item_data)

            if 'data' in result and result['data']:
                return ResponseUtil.success(data=self.model_to_dict(result['data']), msg="添加成功", as_dict=True)

            return ResponseUtil.success(msg="添加成功", as_dict=True)
        except ValueError as e:
            return self._handle_value_error("添加数据", e, "参数校验失败")
        except Exception as e:
            return self._handle_exception("添加数据", e, "添加失败")

    def update_item(self, item_data: dict) -> Any:
        """
        更新数据
        """
        try:
            # 从数据中提取ID
            item_id = item_data.get('id')
            if not item_id:
                return ResponseUtil.failure(msg="缺少ID参数", as_dict=True)

            result = self.service_class().update(item_id, item_data)

            if result.get('success') and 'data' in result and result['data']:
                return ResponseUtil.success(data=self.model_to_dict(result['data']), msg="更新成功", as_dict=True)
            elif not result.get('success'):
                return ResponseUtil.failure(msg=result.get('message', "更新失败"), as_dict=True)

            return ResponseUtil.success(msg="更新成功", as_dict=True)
        except ValueError as e:
            return self._handle_value_error("更新数据", e, "参数校验失败")
        except Exception as e:
            return self._handle_exception("更新数据", e, "更新失败")

    def delete_item(self, item_id: int) -> Any:
        """
        删除数据
        """
        try:
            result = self.service_class().delete(item_id)

            if result.get('success'):
                return ResponseUtil.success(msg="删除成功", as_dict=True)
            else:
                return ResponseUtil.failure(msg=result.get('message', "删除失败"), as_dict=True)
        except Exception as e:
            return self._handle_exception("删除数据", e, "删除失败")

    def get_list_by_filters(self, filters: Optional[Dict[str, Any]] = None) -> Any:
        """
        根据条件获取列表
        """
        try:
            models = self.service_class().get_list_by_filters(filters)
            data = self.models_to_dicts(models)
            return ResponseUtil.success(data=data, as_dict=True)
        except Exception as e:
            return self._handle_exception("根据条件获取列表", e, "获取列表失败")