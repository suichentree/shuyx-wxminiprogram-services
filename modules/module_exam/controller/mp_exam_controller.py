from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter,Body
from config.log_config import logger
from modules.module_exam.service.mp_exam_service import MpExamService
from modules.module_exam.service.mp_option_service import MpOptionService
from modules.module_exam.service.mp_question_service import MpQuestionService
from modules.module_exam.service.mp_user_exam_service import MpUserExamService
from utils.response_util import ResponseUtil

# 创建路由实例
router = APIRouter(prefix='/mp/exam', tags=['mp_exam接口'])
# 创建服务实例
MpExamService_instance = MpExamService()
MpOptionService_instance = MpOptionService()
MpQuestionService_instance = MpQuestionService()
MpUserExamService_instance = MpUserExamService()

"""
获取测试列表信息
"""
@router.get("/getExamList")
def getExamList(page_num:int=1, page_size:int=10):
    logger.info(f'/mp/exam/getExamList, page_num = {page_num}, page_size = {page_size}')
    # 调用服务层方法，查询所有考试信息
    result = MpExamService_instance.get_page_list(page_num=page_num, page_size=page_size)
    # 若result为空，则返回空列表。不为空则返回result
    return ResponseUtil.success(data=result if result is not None else [])


"""
获取测试题目列表信息
"""
@router.post("/getQuestionList")
def getQuestionList(exam_id:int = Body(None,embed=True)):
    logger.info(f'/mp/exam/getQuestionList, exam_id = {exam_id}')

    # 根据examid去查询对应题目
    questionlist = MpQuestionService_instance.get_list_by_filters(filters={"exam_id": exam_id})

    jsonArray = []

    # 遍历题目列表，查询每个题目对应的选项
    for question in questionlist:
        jsonobj = {
            "id": question['id'],
            "exam_id": question['exam_id'],
            "type": question['type'],
            "name": question['name'],
        }

        # 查询选项列表
        optionList = MpOptionService_instance.get_list_by_filters(filters={
            "question_id": question['id']
        })
        jsonArray2 = []
        for option in optionList:
            jsonArray2.append({
                "id": option['id'],
                "content": option['content'],
                "question_id": option['question_id'],
            })

        jsonobj["options"] = jsonArray2

        # 将选项列表添加到题目字典中
        jsonArray.append(jsonobj)

    return ResponseUtil.success(data=jsonArray)



"""
获取测试进度信息
"""
@router.post("/getExamProgress")
def getExamProgress(user_id:int = Body(None),exam_id:int = Body(None)):
    logger.info(f'/mp/exam/getExamProgress, user_id = {user_id}, exam_id = {exam_id}')
    # 调用服务层方法，查询考试进度信息
    result = MpUserExamService_instance.get_one_by_filters(filters={
        "user_id": user_id,
        "exam_id": exam_id
    })
    # 返回测试进度
    if result is not None:
        return ResponseUtil.success(data={"exam_pageNo": result['page_no']})
    else:
        return ResponseUtil.success(data={"exam_pageNo": 0})

"""
单选题答题
"""
@router.post("/danxueAnswer")
def danxueAnswer(userId = Body(...),examId = Body(...),questionId = Body(...),optionId = Body(...),pageNo = Body(...)):
    logger.info(f'/mp/exam/danxueAnswer, userId = {userId}, examId = {examId}, questionId = {questionId}, optionId = {optionId}, pageNo = {pageNo}')

    # 查询选项信息
    option_result = MpOptionService_instance.get_by_id({"option_id": optionId})
    if option_result is None:
        return ResponseUtil.error(msg="选项不存在")

    # 查询题目个数
    question_count = MpQuestionService_instance.get_list_by_filters(filters={
        "examId": examId
    }).count()

    # 查询用户是否有没做完的测试记录
    exam_result = MpExamService_instance.get_one_by_filters(filters={
        "userId": userId,
        "examId": examId,
        "is_finished": 0
    })

    if exam_result is None:
        logger.info(f'用户 userId = {userId}, examId = {examId}, 无未做完测试，创建新的测试记录')
        # 创建新的测试记录
        MpExamService_instance.add({
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
    useroption_result = MpOptionService_instance.add(new_useroption)
    # 返回新创建的用户选项信息
    return ResponseUtil.success(data=useroption_result if useroption_result is not None else None)

"""
多选题答题
"""
@router.post("/duoxueAnswer")
def duoxue_Answer(userId = Body(...),examId = Body(...),questionId = Body(...),optionIds = Body(...),pageNo = Body(...)):
    logger.info(f'/mp/exam/duoxueAnswer, user_id = {userId}, exam_id = {examId}, question_id = {questionId}, option_ids = {optionIds}, page_no = {pageNo}')
    # 查询题目的正确选项集合
    option_result:List[Dict[str,Any]] = MpOptionService_instance.get_list_by_filters(filters={
        "questionId": questionId,
        "score": 1
    })



