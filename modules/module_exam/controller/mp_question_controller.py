from fastapi import APIRouter
from config.log_config import logger
from modules.module_exam.service.mp_question_service import MpQuestionService
from utils.response_util import ResponseUtil
from utils.controller_util import model_to_dict, models_to_dicts, handle_exceptions

# 创建路由实例
router = APIRouter(prefix='/mp/question', tags=['mp_question接口'])
# 创建服务实例
mpQuestionService = MpQuestionService()

@router.get("/test")
async def test(page_size:int,page_num:int):
    logger.info(f'/mp/question/test, page_size = {page_size} page_num = {page_num}')
    return {
        page_num:page_num,
        page_size:page_size
    }

@router.get("/get_page_list")
@handle_exceptions("分页获取题目列表", "获取题目列表失败")
async def get_page_list(page_size:int,page_num:int):
    logger.info(f'/mp/question/get_page_list, page_size = {page_size} page_num = {page_num}')

    # 使用实例方法调用服务
    result = mpQuestionService.get_page_list(page_num, page_size)
    # 确保正确处理响应格式
    if isinstance(result, dict) and 'data' in result:
        # 转换模型数据为字典数据
        if result['data']:
            result['data'] = models_to_dicts(result['data'])

        return ResponseUtil.success(
            data=result['data'],
            dict_content={'total': result.get('total', 0)},
            as_dict=True
        )

    return ResponseUtil.success(data=result, as_dict=True)

@router.get("/get_by_id/{question_id}")
@handle_exceptions("获取题目详情", "获取题目详情失败")
async def get_by_id(question_id: int):
    logger.info(f'/mp/question/get_by_id, question_id = {question_id}')
    logger.info(f'/mp/question/get_by_id, question_id = {question_id}')

    # 使用实例方法调用服务
    result = mpQuestionService.get_by_id(question_id)

    if not result:
        return ResponseUtil.failure(msg="题目不存在", as_dict=True)

    return ResponseUtil.success(data=model_to_dict(result), as_dict=True)


@router.get("/get_list_by_filters")
@handle_exceptions("条件查询题目", "条件查询题目失败")
async def get_list_by_filters(
        exam_id: int,
        question_type: int,
        is_enabled: bool
):
    """
    根据条件查询题目列表
    """
    # 构建过滤条件
    filters = {}
    if exam_id is not None:
        filters['exam_id'] = exam_id
    if question_type is not None:
        filters['type'] = question_type
    if is_enabled is not None:
        filters['is_enabled'] = is_enabled

    logger.info(f'/mp/question/get_list_by_filters, filters = {filters}')

    # 调用服务层获取数据
    models = mpQuestionService.get_list_by_filters(filters)
    data = models_to_dicts(models)

    return ResponseUtil.success(data=data, as_dict=True)


@router.post("/add_item")
@handle_exceptions("添加题目", "添加题目失败")
async def add_item(item_data: dict):
    """
    添加新题目
    """
    logger.info(f'/mp/question/add_item, item_data = {item_data}')

    # 使用实例方法调用服务
    result = mpQuestionService.add(item_data)

    if isinstance(result, dict) and 'data' in result and result['data']:
        return ResponseUtil.success(
            data=model_to_dict(result['data']),
            msg="添加成功",
            as_dict=True
        )

    return ResponseUtil.success(msg="添加成功", as_dict=True)


@router.put("/update_item")
@handle_exceptions("更新题目", "更新题目失败")
async def update_item(item_data: dict):
    """
    更新题目信息
    """
    # 验证ID是否存在
    item_id = item_data.get('id')
    if not item_id:
        return ResponseUtil.failure(msg="缺少ID参数", as_dict=True)

    logger.info(f'/mp/question/update_item, item_id = {item_id}, item_data = {item_data}')

    # 使用实例方法调用服务
    result = mpQuestionService.update(item_id, item_data)

    if isinstance(result, dict):
        if result.get('success') and 'data' in result and result['data']:
            return ResponseUtil.success(
                data=model_to_dict(result['data']),
                msg="更新成功",
                as_dict=True
            )
        elif not result.get('success'):
            return ResponseUtil.failure(
                msg=result.get('message', "更新失败"),
                as_dict=True
            )

    return ResponseUtil.success(msg="更新成功", as_dict=True)


@router.delete("/delete_item/{question_id}")
@handle_exceptions("删除题目", "删除题目失败")
async def delete_item(question_id: int):
    """
    删除题目
    """
    logger.info(f'/mp/question/delete_item, question_id = {question_id}')

    # 使用实例方法调用服务
    result = mpQuestionService.delete(question_id)

    if isinstance(result, dict):
        if result.get('success'):
            return ResponseUtil.success(msg="删除成功", as_dict=True)
        else:
            return ResponseUtil.failure(
                msg=result.get('message', "删除失败"),
                as_dict=True
            )

    # 兼容简单布尔返回值
    if result:
        return ResponseUtil.success(msg="删除成功", as_dict=True)
    else:
        return ResponseUtil.failure(msg="删除失败", as_dict=True)





