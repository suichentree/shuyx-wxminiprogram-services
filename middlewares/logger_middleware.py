from fastapi import Request
import time
from loguru import logger
from typing import Callable

# 日志中间件
async def LoggerMiddleware(request: Request, call_next: Callable):
    print("LoggerMiddleware========================")

    # 请求开始时间
    start_time = time.time()

    # 记录请求信息
    logger.info(f"Request: {request.method} {request.url.path}")

    # 继续处理请求，并获取响应对象
    response = await call_next(request)

    # 计算处理时间
    process_time = time.time() - start_time

    # 记录响应信息
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")

    # 添加响应时间到头部
    response.headers["X-Process-Time"] = str(process_time)

    return response