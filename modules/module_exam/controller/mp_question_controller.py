from fastapi import APIRouter
from config.log_config import logger
from modules.module_exam.service.mp_question_service import MpQuestionService
from utils.response_util import ResponseUtil

# 创建路由实例
router = APIRouter(prefix='/mp/question', tags=['mp_question接口'])
# 创建服务实例
mpQuestionService = MpQuestionService()

@router.get("/testexception")
async def testexception():
    logger.info(f'/mp/question/testexception')
    raise Exception("测试异常11111")


@router.get("/get_page_list")
async def get_page_list(page_size:int,page_num:int):
    logger.info(f'/mp/question/get_page_list, page_size = {page_size} page_num = {page_num}')
    # 使用实例方法调用服务
    result = mpQuestionService.get_page_list(page_num, page_size)
    print(type(result))
    print(f"result = {result}")
    return ResponseUtil.success(data=result)


@router.get("/get_by_id/{question_id}")
async def get_by_id(question_id: int):
    logger.info(f'/mp/question/get_by_id, question_id = {question_id}')

    # 使用实例方法调用服务
    result = mpQuestionService.get_by_id(question_id)
    # 返回
    return ResponseUtil.success(data=result)


@router.get("/get_list_by_filters")
async def get_list_by_filters(filters: dict):
    logger.info(f'/mp/question/get_list_by_filters, filters = {filters}')
    # 调用服务层获取数据
    result = mpQuestionService.get_list_by_filters(filters)
    return ResponseUtil.success(data=result)

@router.post("/add_item")
async def add_item(item_data: dict):
    """
    添加新题目
    """
    logger.info(f'/mp/question/add_item, item_data = {item_data}')

    # 使用实例方法调用服务
    result = mpQuestionService.add(item_data)
    return ResponseUtil.success(message="添加新题目成功")


@router.put("/update_item")
async def update_item(item_data: dict):
    """
    更新题目信息
    """
    logger.info(f'/mp/question/update_item,item_data = {item_data}')
    # 验证ID是否存在
    item_id = item_data.get('id')
    if not item_id:
        return ResponseUtil.error(code=400, message="缺少ID参数")

    # 使用实例方法调用服务
    result = mpQuestionService.update(item_id, item_data)
    return ResponseUtil.success(data=result,message="更新题目成功")


@router.delete("/delete_item/{question_id}")
async def delete_item(question_id: int):
    """
    删除题目
    """
    logger.info(f'/mp/question/delete_item, question_id = {question_id}')

    # 使用实例方法调用服务
    result = mpQuestionService.delete(question_id)
    # 兼容简单布尔返回值
    if result:
        return ResponseUtil.success(message="删除成功")
    else:
        return ResponseUtil.error(message="删除失败")





