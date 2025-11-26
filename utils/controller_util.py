from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta
from config.log_config import logger
from utils.response_util import ResponseUtil

def model_to_dict(model: DeclarativeMeta) -> Dict[str, Any]:
    """
    将SQLAlchemy模型转换为字典
    """
    result = {}
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        if isinstance(value, datetime):
            result[column.name] = str(value)
        else:
            result[column.name] = value
    return result

def models_to_dicts(models: List[DeclarativeMeta]) -> List[Dict[str, Any]]:
    """
    将模型列表转换为字典列表
    """
    return [model_to_dict(model) for model in models]

# 同步函数异常处理装饰器
def handle_exceptions_sync(func_name: str, default_msg: str):
    """
    同步函数异常处理装饰器
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"{func_name}失败: {str(e)}")
                return ResponseUtil.error(msg=f"{default_msg}: {str(e)}", as_dict=True)
        return wrapper
    return decorator

# 异步函数异常处理装饰器
def handle_exceptions(func_name: str, default_msg: str):
    """
    异步函数异常处理装饰器
    """
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"{func_name}失败: {str(e)}")
                return ResponseUtil.error(msg=f"{default_msg}: {str(e)}", as_dict=True)
        return wrapper
    return decorator