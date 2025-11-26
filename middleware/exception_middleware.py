from fastapi import Request
from fastapi.responses import JSONResponse
from config.log_config import logger
from utils.response_util import ResponseUtil


async def global_exception_handler(request: Request, exc: Exception):
    """
    全局异常处理中间件
    """
    path = request.url.path
    logger.exception(f"请求 {path} 发生异常: {str(exc)}")

    # 根据异常类型返回不同的错误信息
    return JSONResponse(
        status_code=500,
        content=ResponseUtil.error(
            msg=f"服务器内部错误: {str(exc)}",
            code=500,
            as_dict=True
        )
    )


# 可以添加更多特定类型的异常处理器
def register_exception_handlers(app):
    """
    注册所有异常处理器
    """
    # 全局异常处理器
    app.add_exception_handler(Exception, global_exception_handler)

    # 可以添加其他特定类型的异常处理器
    # app.add_exception_handler(ValueError, value_error_handler)
    # app.add_exception_handler(HTTPException, http_exception_handler)