from datetime import datetime
from typing import List, Dict, Any

from fastapi import APIRouter,Body
from config.log_config import logger
from modules.module_exam.model.mp_exam_model import MpExamModel
from modules.module_exam.model.mp_option_model import MpOptionModel
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
def danxueAnswer(userId = Body(...),examId = Body(...),questionId = Body(...),optionId = Body(...),pageNo = Body(...)):
    logger.info(f'/mp/exam/danxueAnswer, userId = {userId}, examId = {examId}, questionId = {questionId}, optionId = {optionId}, pageNo = {pageNo}')

    # 查询选项信息
    option_result = option_service.get_by_id({"option_id": optionId})
    if option_result is None:
        return ResponseUtil.error(msg="选项不存在")

    # 查询题目个数
    question_count = question_service.get_list_by_filters(filters={
        "examId": examId
    }).count()

    # 查询用户是否有没做完的测试记录
    exam_result = service.get_one_by_filters(filters={
        "userId": userId,
        "examId": examId,
        "is_finished": 0
    })

    if exam_result is None:
        logger.info(f'用户 userId = {userId}, examId = {examId}, 无未做完测试，创建新的测试记录')
        # 创建新的测试记录
        service.add({
            "userId": userId,
            "examId": examId,
            "page_no": pageNo,
            "score": option_result['score'],
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    else:
        logger.info(f'用户 userId = {userId}, examId = {examId}, 有未做完测试，继续测试')
        exam_result['score'] += option_result['score']
        exam_result['page_no'] = pageNo
        # 若题号和题目数相等，则表示这是最后一题
        if pageNo == question_count:
            exam_result['finish_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 创建新的用户选项信息
    new_useroption = {
        "userId": userId,
        "examId": examId,
        "isDuoxue": 0,
        "questionId": questionId,
        "optionId": optionId,
        "isRight": 1 if option_result['is_right'] == 1 else 0,
    }
    useroption_result = option_service.add(new_useroption)
    # 返回新创建的用户选项信息
    return ResponseUtil.success(data=useroption_result if useroption_result is not None else None)

"""
多选题答题
"""
@router.post("/duoxueAnswer")
def duoxue_Answer(userId = Body(...),examId = Body(...),questionId = Body(...),optionIds = Body(...),pageNo = Body(...)):
    logger.info(f'/mp/exam/duoxueAnswer, user_id = {userId}, exam_id = {examId}, question_id = {questionId}, option_ids = {optionIds}, page_no = {pageNo}')
    # 查询题目的正确选项集合
    option_result:List[Dict[str,Any]] = option_service.get_list_by_filters(filters={
        "questionId": questionId,
        "score": 1
    })



