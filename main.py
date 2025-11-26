# 导入FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 导入控制器路由
from modules.module_exam.controller.mp_exam_controller import router as mp_exam_router
from modules.module_exam.controller.mp_question_controller import router as mp_question_router

# 导入配置
from config.log_config import logger

# 创建FastAPI应用实例
app = FastAPI(
    title="微信小程序服务API",
    description="微信小程序-测试系统后端API",
    version="1.0.1"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 通过include_router函数，把各个路由实例加入到FastAPI应用实例中,进行统一管理
app.include_router(mp_exam_router)
app.include_router(mp_question_router)

# 测试接口
@app.get("/")
async def root():
    """根路径接口"""
    return {"message": "Hello World , 服务运行正常", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        app='main:app',
        port=39666,
        reload=True,
        log_level="info"  # 添加日志级别配置
    )