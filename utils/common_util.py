from typing import Generic, TypeVar, List, Dict, Any, Optional, Union
from datetime import datetime
import inspect

# 定义类型变量
ModelType = TypeVar('ModelType')


class CommonUtil:
    """
    通用工具类，提供数据转换和其他通用功能
    专注于将SQLAlchemy模型等复杂对象转换为可序列化的格式
    """

    @staticmethod
    def model_to_dict(model: Any) -> Optional[Dict[str, Any]]:
        """
        将SQLAlchemy模型转换为字典

        Args:
            model: SQLAlchemy模型实例或其他对象

        Returns:
            Dict[str, Any]或None: 转换后的字典，如果输入为None则返回None
        """
        if model is None:
            return None

        # 检查是否是SQLAlchemy模型（有__table__属性）
        if hasattr(model, '__table__'):
            result = {}
            for column in model.__table__.columns:
                value = getattr(model, column.name)
                # 递归转换复杂类型
                result[column.name] = CommonUtil.convert_to_serializable(value)
            return result

        # 对于非SQLAlchemy对象，尝试获取其公共属性
        result = {}
        for name, value in inspect.getmembers(model):
            # 跳过私有属性和方法
            if not name.startswith('_') and not inspect.ismethod(value) and not inspect.isfunction(value):
                try:
                    result[name] = CommonUtil.convert_to_serializable(value)
                except:
                    # 无法序列化的属性跳过
                    pass
        return result

    @staticmethod
    def models_to_dicts(models: Union[List[Any], Any]) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
        """
        将模型列表或单个模型转换为字典列表或字典
        自动检测输入类型并进行相应转换

        Args:
            models: 模型实例列表或单个模型实例

        Returns:
            List[Dict[str, Any]]或Dict[str, Any]或None: 转换后的结果
        """
        if models is None:
            return None

        # 如果是列表，批量转换
        if isinstance(models, list):
            return [CommonUtil.model_to_dict(model) for model in models]

        # 单个模型，直接转换
        return CommonUtil.model_to_dict(models)

    @staticmethod
    def convert_to_serializable(data: Any) -> Any:
        """
        递归转换数据为可JSON序列化的格式
        处理各种复杂类型，包括SQLAlchemy模型、datetime、列表、字典等

        Args:
            data: 任意类型的数据

        Returns:
            可JSON序列化的数据
        """
        if data is None:
            return None

        # 处理SQLAlchemy模型
        if hasattr(data, '__table__'):
            return CommonUtil.model_to_dict(data)

        # 处理datetime
        elif isinstance(data, datetime):
            return data.strftime('%Y-%m-%d %H:%M:%S')  # 更规范的时间格式

        # 处理日期（无时间部分）
        elif hasattr(data, 'strftime'):
            try:
                return data.strftime('%Y-%m-%d')
            except:
                return str(data)

        # 处理列表
        elif isinstance(data, list):
            return [CommonUtil.convert_to_serializable(item) for item in data]

        # 处理字典
        elif isinstance(data, dict):
            return {key: CommonUtil.convert_to_serializable(value)
                    for key, value in data.items()}

        # 处理SQLAlchemy查询结果（可能是Row对象）
        elif hasattr(data, '_asdict'):
            return data._asdict()

        # 处理其他可序列化的基本类型
        elif isinstance(data, (str, int, float, bool)):
            return data

        # 其他类型转换为字符串
        else:
            return str(data)

    @staticmethod
    def convert_paginated_result(paginated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        专门处理分页结果的数据转换

        Args:
            paginated_data: 包含分页信息的字典，如{"data": [...], "total": 100, ...}

        Returns:
            Dict[str, Any]: 转换后的分页数据
        """
        if not isinstance(paginated_data, dict):
            return paginated_data

        result = paginated_data.copy()
        # 转换data字段中的模型数据
        if 'data' in result:
            result['data'] = CommonUtil.models_to_dicts(result['data'])
        return result


# 测试示例
if __name__ == '__main__':
    print("CommonUtil类已定义，可以用于数据转换")
