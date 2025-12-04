from datetime import datetime

from fastapi import APIRouter,Body
from config.log_config import logger
from modules.module_exam.model.mp_exam_model import MpExamModel
from modules.module_exam.service.mp_exam_service import MpExamService
from modules.module_exam.service.mp_option_service import MpOptionService
from modules.module_exam.service.mp_question_service import MpQuestionService
from utils.response_util import ResponseUtil

# 创建路由实例
router = APIRouter(prefix='/mp/exam', tags=['mp_exam接口'])
# 创建服务实例
service = MpExamService()
option_service = MpOptionService()
question_service = MpQuestionService()

"""
获取测试列表信息
"""
@router.get("/getExamList")
def getExamList(page_num:int=1, page_size:int=10):
    logger.info(f'/mp/exam/getExamList, page_num = {page_num}, page_size = {page_size}')
    # 调用服务层方法，查询所有考试信息
    result = service.get_page_list(page_num=page_num, page_size=page_size)
    # 若result为空，则返回空列表。不为空则返回result
    return ResponseUtil.success(data=result if result is not None else [])

"""
获取测试进度信息
"""
@router.get("/getExamProgress")
def getExamProgress(user_id:int,exam_id:int):
    logger.info(f'/mp/exam/getExamProgress, user_id = {user_id}, exam_id = {exam_id}')
    # 调用服务层方法，查询考试进度信息
    result = service.get_one_by_filters(filters={
        "user_id": user_id,
        "exam_id": exam_id
    })
    # 若result为空，则返回空列表。不为空则返回result
    return ResponseUtil.success(data=result if result is not None else [])

"""
获取测试题目信息
"""
@router.get("/getExamProgress")
def getQuestionList(exam_id:int):
    logger.info(f'/mp/exam/getQuestionList, exam_id = {exam_id}')
    # 调用服务层方法，查询考试题目信息
    result = service.get_list_by_filters(filters={
        "exam_id": exam_id
    })
    # 若result为空，则返回空列表。不为空则返回result
    return ResponseUtil.success(data=result if result is not None else [])


"""
单选题答题
"""
@router.post("/danxueAnswer")
def danxueAnswer(user_id = Body(...),exam_id = Body(...),question_id = Body(...),option_id = Body(...),page_no = Body(...)):
    logger.info(f'/mp/exam/danxueAnswer, user_id = {user_id}, exam_id = {exam_id}, question_id = {question_id}, option_id = {option_id}, page_no = {page_no}')

    # 查询选项信息
    option_result = option_service.get_by_id({"option_id": option_id})
    if option_result is None:
        return ResponseUtil.error(msg="选项不存在")

    # 查询题目个数
    question_count = question_service.get_list_by_filters(filters={
        "exam_id": exam_id
    }).count()

    # 查询用户是否有没做完的测试记录
    exam_result: MpExamModel = service.get_one_by_filters(filters={
        "user_id": user_id,
        "exam_id": exam_id,
        "is_finished": False
    })

    if exam_result is None:
        logger.info(f'用户 user_id = {user_id}, exam_id = {exam_id}, 无未做完测试，创建新的测试记录')
        # 创建新的测试记录
        service.add({
            "user_id": user_id,
            "exam_id": exam_id,
            "page_no": page_no,
            "score": option_result['score'],
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    else:
        logger.info(f'用户 user_id = {user_id}, exam_id = {exam_id}, 有未做完测试，继续测试')
        exam_result['score'] += option_result['score']
        exam_result['page_no'] = page_no
        # 若题号和题目数相等，则表示这是最后一题
        if page_no == question_count:
            exam_result['finish_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        # 检查是否超过了测试时间
        exam_end_time = exam_no_finish_result["exam_end_time"]
        if datetime.now() > exam_end_time:
            return ResponseUtil.error(msg="测试时间已过")






    # 调用服务层方法，查询考试题目信息
    result = service.get_one_by_filters(filters={
        "user_id": user_id,
        "exam_id": exam_id,
        "question_id": question_id
    })
    # 若result为空，则返回空列表。不为空则返回result
    return ResponseUtil.success(data=result if result is not None else [])
