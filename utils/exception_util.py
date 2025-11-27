from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from main import app

# 自定义异常类
class ExceptionUtil(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)

# 注册自定义异常处理器
# 当抛出ExceptionUtil异常时，调用该处理器返回自定义的JSON响应
@app.exception_handler(ExceptionUtil)
async def exception_handler(request: Request, exc: ExceptionUtil):
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "message": exc.message, "data": None}
    )

# 在业务代码中使用
if __name__ == "__main__":
    print(ExceptionUtil(code=400, message="无效的项目ID"))
    print(type(ExceptionUtil(code=400, message="无效的项目ID")))
    raise ExceptionUtil(code=400, message="无效的项目ID")
