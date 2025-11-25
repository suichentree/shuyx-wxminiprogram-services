from fastapi import Body
from .base_controller import BaseController
from ..service.mp_exam_service import MpExamService
from ..model.mp_exam_model import MpExamModel
from config.log_config import logger
from utils.response_util import ResponseUtil

class MpExamController(BaseController[MpExamModel, MpExamService]):
    """
    考试控制器
    """

    def __init__(self):
        """
        初始化考试控制器
        """
        super().__init__(
            service_class=MpExamService,
            model_class=MpExamModel,
            prefix="/mp_exam",
            tags=["mp_exam"]
        )
        self._register_routes()

    def _register_routes(self):
        """
        注册路由
        """
        # 基础路由
        self.router.post("/get_page_list")(self.get_page_list_route)
        self.router.get("/get_by_id/{exam_id}")(self.get_by_id_route)
        self.router.post("/add")(self.add_exam_route)
        self.router.post("/update")(self.update_exam_route)
        self.router.delete("/delete/{exam_id}")(self.delete_exam_route)

        # 扩展路由
        self.router.get("/get_by_type/{exam_type}")(self.get_by_type_route)
        self.router.get("/get_active")(self.get_active_exams_route)

    async def get_page_list_route(self, pageSize: int = Body(..., description="每页大小"),
                                  pageNum: int = Body(..., description="页码")):
        """
        分页获取考试列表
        """
        logger.info(f'/mp_exam/get_page_list, pageSize = {pageSize}, pageNum = {pageNum}')
        return self.get_page_list(page_num=pageNum, page_size=pageSize)

    async def get_by_id_route(self, exam_id: int):
        """
        根据ID获取考试详情
        """
        logger.info(f'/mp_exam/get_by_id, exam_id = {exam_id}')
        return self.get_by_id(item_id=exam_id)

    async def add_exam_route(self, exam_data: dict = Body(...)):
        """
        添加考试
        """
        logger.info(f'/mp_exam/add, exam_data = {exam_data}')
        return self.add_item(item_data=exam_data)

    async def update_exam_route(self, exam_data: dict = Body(...)):
        """
        更新考试信息
        """
        logger.info(f'/mp_exam/update, exam_data = {exam_data}')
        return self.update_item(item_data=exam_data)

    async def delete_exam_route(self, exam_id: int):
        """
        删除考试
        """
        logger.info(f'/mp_exam/delete, exam_id = {exam_id}')
        return self.delete_item(item_id=exam_id)

    async def get_by_type_route(self, exam_type: str):
        """
        根据类型获取考试列表
        """
        logger.info(f'/mp_exam/get_by_type, exam_type = {exam_type}')
        try:
            # 调用服务层获取数据
            models = MpExamService().get_exams_by_type(exam_type)

            # 转换数据模型为字典列表
            data = self.models_to_dicts(models)
            return ResponseUtil.success(data=data)
        except Exception as e:
            logger.exception(f"根据类型获取考试列表失败: {str(e)}")
            return ResponseUtil.error(msg=f"根据类型获取考试列表失败: {str(e)}")

    async def get_active_exams_route(self):
        """
        获取未禁用的考试列表
        """
        logger.info(f'/mp_exam/get_active')
        try:
            # 调用服务层获取数据
            models = MpExamService().get_active_exams()

            # 转换数据模型为字典列表
            data = self.models_to_dicts(models)
            return ResponseUtil.success(data=data)
        except Exception as e:
            logger.exception(f"获取未禁用考试列表失败: {str(e)}")
            return ResponseUtil.error(msg=f"获取未禁用考试列表失败: {str(e)}")


# 创建控制器实例
controller = MpExamController()
router = controller.router