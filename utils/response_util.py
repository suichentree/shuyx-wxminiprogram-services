from fastapi import status
from fastapi.responses import JSONResponse, Response, StreamingResponse
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, Optional
from pydantic import BaseModel
from datetime import datetime


class ResponseUtil:
    """
    响应工具类
    提供统一的响应格式和便捷的响应方法
    """

    @classmethod
    def _create_response_dict(cls, code: int, msg: str, success: bool = True,
                              data: Optional[Any] = None, **kwargs) -> Dict[str, Any]:
        """
        创建响应字典

        Args:
            code: 响应码
            msg: 响应消息
            success: 是否成功
            data: 响应数据
            **kwargs: 其他响应字段

        Returns:
            Dict[str, Any]: 响应字典
        """
        result = {
            'code': code,
            'msg': msg,
            'success': success,
            'time': datetime.now()
        }

        if data is not None:
            result['data'] = data

        result.update(kwargs)
        return result

    @classmethod
    def success(cls, msg: str = '操作成功', data: Optional[Any] = None,
                as_dict: bool = False, **kwargs) -> Any:
        """
        成功响应

        Args:
            msg: 响应消息
            data: 响应数据
            as_dict: 是否返回字典而不是Response对象
            **kwargs: 其他响应字段

        Returns:
            Union[Dict, Response]: 响应字典或Response对象
        """
        result = cls._create_response_dict(200, msg, True, data, **kwargs)
        return result if as_dict else JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(result)
        )

    @classmethod
    def failure(cls, msg: str = '操作失败', data: Optional[Any] = None,
                as_dict: bool = False, code: int = 601, **kwargs) -> Any:
        """
        失败响应

        Args:
            msg: 响应消息
            data: 响应数据
            as_dict: 是否返回字典而不是Response对象
            code: 响应码，默认601
            **kwargs: 其他响应字段

        Returns:
            Union[Dict, Response]: 响应字典或Response对象
        """
        result = cls._create_response_dict(code, msg, False, data, **kwargs)
        return result if as_dict else JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(result)
        )

    @classmethod
    def error(cls, msg: str = '接口异常', data: Optional[Any] = None,
              as_dict: bool = False, **kwargs) -> Any:
        """
        错误响应

        Args:
            msg: 响应消息
            data: 响应数据
            as_dict: 是否返回字典而不是Response对象
            **kwargs: 其他响应字段

        Returns:
            Union[Dict, Response]: 响应字典或Response对象
        """
        return cls.failure(msg, data, as_dict, 500, **kwargs)

    @classmethod
    def unauthorized(cls, msg: str = '登录信息已过期，访问系统资源失败',
                     data: Optional[Any] = None, as_dict: bool = False, **kwargs) -> Any:
        """
        未授权响应

        Args:
            msg: 响应消息
            data: 响应数据
            as_dict: 是否返回字典而不是Response对象
            **kwargs: 其他响应字段

        Returns:
            Union[Dict, Response]: 响应字典或Response对象
        """
        return cls.failure(msg, data, as_dict, 401, **kwargs)

    @classmethod
    def forbidden(cls, msg: str = '该用户无此接口权限',
                  data: Optional[Any] = None, as_dict: bool = False, **kwargs) -> Any:
        """
        禁止访问响应

        Args:
            msg: 响应消息
            data: 响应数据
            as_dict: 是否返回字典而不是Response对象
            **kwargs: 其他响应字段

        Returns:
            Union[Dict, Response]: 响应字典或Response对象
        """
        return cls.failure(msg, data, as_dict, 403, **kwargs)

    @classmethod
    def streaming(cls, data: Any = None) -> StreamingResponse:
        """
        流式响应

        Args:
            data: 流式传输的内容

        Returns:
            StreamingResponse: 流式响应对象
        """
        return StreamingResponse(
            status_code=status.HTTP_200_OK,
            content=data
        )