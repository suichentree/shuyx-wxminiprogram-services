from functools import wraps
from typing import Callable, Any
from utils.response_util import ResponseUtil

def standard_response(success_msg: str = "操作成功"):
    """
    统一响应格式装饰器
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            # 如果已经是ResponseUtil返回的格式，直接返回
            if isinstance(result, dict) and ('code' in result or 'success' in result):
                return result
            # 否则包装为标准格式
            return ResponseUtil.success(data=result, msg=success_msg, as_dict=True)
        return wrapper
    return decorator
