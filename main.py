# 导入FastAPI
from fastapi import FastAPI
import uvicorn
from modules.module_exam.controller.mp_exam_controller import router as mp_exam_router

# 创建FastAPI应用实例
app = FastAPI()
# 通过include_router函数，把各个路由实例加入到FastAPI应用实例中,进行统一管理
app.include_router(mp_exam_router,prefix="/mp_exam",tags=["exam模块的接口"])

# 测试接口
@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(
        app='main:app',
        port=39666,
        reload=True
    )