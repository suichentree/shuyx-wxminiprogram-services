from starlette.responses import JSONResponse

# 自定义异常类
class ExceptionUtil(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(self.code,self.message)

# 注册自定义异常处理器到FastAPI应用实例
# 通过函数方式延迟注册，避免循环导入问题
def register_exception_handlers(app):
    # 当抛出ExceptionUtil异常时，调用该处理器返回 ResponseUtil.exception方法创建的异常响应对象
    @app.exception_handler(ExceptionUtil)
    async def exception_util_handler(exc: ExceptionUtil):
        # 返回异常信息
        return JSONResponse(
            status_code=exc.code,
            content={"code": exc.code, "message": exc.message}
        )

# 在业务代码中使用
if __name__ == "__main__":
    # 示例：异常使用
    try:
        # 抛出业务异常
        raise ExceptionUtil(code=500, message="测试异常")
    except ExceptionUtil as e:
        print(f"异常: {e}")
