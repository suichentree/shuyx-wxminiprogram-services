from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter,Body
from config.log_config import logger
from modules.module_exam.service.mp_exam_service import MpExamService
from modules.module_exam.service.mp_option_service import MpOptionService
from modules.module_exam.service.mp_question_service import MpQuestionService
from modules.module_exam.service.mp_user_exam_service import MpUserExamService
from modules.module_exam.service.mp_user_option_service import MpUserOptionService
from utils.response_util import ResponseUtil

# 创建路由实例
router = APIRouter(prefix='/mp/exam', tags=['mp_exam接口'])
# 创建服务实例
MpExamService_instance = MpExamService()
MpOptionService_instance = MpOptionService()
MpQuestionService_instance = MpQuestionService()
MpUserExamService_instance = MpUserExamService()
MpUserOptionService_instance = MpUserOptionService()


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
            "questionId": question['id'],
            "examId": question['exam_id'],
            "questionType": question['type'],
            "name": question['name'],
        }

        # 查询选项列表
        optionList = MpOptionService_instance.get_list_by_filters(filters={
            "question_id": question['id']
        })
        jsonArray2 = []
        for option in optionList:
            jsonArray2.append({
                "optionId": option['id'],
                "content": option['content'],
                "questionId": option['question_id'],
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
@router.post("/danxue_Answer")
def danxueAnswer(userId = Body(None),examId = Body(None),questionId = Body(None),optionId = Body(None),pageNo = Body(None)):
    logger.info(f'/mp/exam/danxue_Answer, userId = {userId}, examId = {examId}, questionId = {questionId}, optionId = {optionId}, pageNo = {pageNo}')

    # 查询选项信息
    option_result = MpOptionService_instance.get_by_id(id=optionId)
    # 根据exam_id查询某个测试的题目个数
    question_count = MpQuestionService_instance.get_total(filters={
        "exam_id": examId
    })
    # 查询用户是否有没做完的测试记录
    user_exam_result = MpUserExamService_instance.get_one_by_filters(filters={
        "user_id": userId,
        "exam_id": examId,
        "finish_time": None
    })
    if user_exam_result is None:
        logger.info(f'用户 userId = {userId}, examId = {examId}, 无未做完测试，创建新的测试记录')
        # 创建新的测试记录
        MpExamService_instance.add({
            "user_id": userId,
            "exam_id": examId,
            "page_no": pageNo,
            "score": option_result['score'],
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    else:
        logger.info(f'用户 userId = {userId}, examId = {examId}, 有未做完测试，继续测试')
        user_exam_result['score'] += user_exam_result['score']
        user_exam_result['page_no'] = pageNo
        # 若题号和题目数相等，则表示这是最后一题,还需要更新finish_time
        if pageNo == question_count:
            user_exam_result['finish_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 更新测试记录
        MpExamService_instance.update_by_id(id=user_exam_result['id'],data=user_exam_result)

    # 创建新的用户选项信息
    new_useroption = {
        "user_id": userId,
        "exam_id": examId,
        "is_duoxue": 0,
        "question_id": questionId,
        "option_id": optionId,
        "is_right": 1 if option_result['score'] == 1 else 0,
    }
    # 新增新的用户选项记录
    MpOptionService_instance.add(new_useroption)

    return ResponseUtil.success()

"""
多选题答题
"""
@router.post("/duoxue_Answer")
def duoxue_Answer(userId = Body(None),examId = Body(None),questionId = Body(None),optionIds = Body(None),pageNo = Body(None)):
    logger.info(f'/mp/exam/duoxue_Answer, user_id = {userId}, exam_id = {examId}, question_id = {questionId}, option_ids = {optionIds}, page_no = {pageNo}')

    # 查询题目的正确选项集合
    rightIds:List[Dict[str,Any]] = MpOptionService_instance.get_list_by_filters(filters={
        "question_id": questionId,
        "score": 1
    })

    # 将正确的选项集合与用户选项的数组进行对比
    isSame:bool = None
    if rightIds == optionIds:
        isSame = True
    else:
        isSame = False

    logger.info(f'用户选择的选项 optionIds = {optionIds}, 多选题目的正确选项 = {rightIds}, 是否相同 = {isSame}')

    # 根据exam_id查询某个测试的题目个数
    question_count = MpQuestionService_instance.get_total(filters={
        "exam_id": examId
    })
    # 查询用户是否有没做完的测试记录
    exam_result = MpExamService_instance.get_one_by_filters(filters={
        "user_id": userId,
        "exam_id": examId,
        "finish_time": None
    })
    if exam_result is None:
        logger.info(f'用户 userId = {userId}, examId = {examId}, 无未做完测试，创建新的测试记录')
        # 创建新的测试记录
        MpExamService_instance.add({
            "user_id": userId,
            "exam_id": examId,
            "page_no": pageNo,
            "score": 1 if isSame else 0,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    else:
        logger.info(f'用户 userId = {userId}, examId = {examId}, 有未做完测试，继续测试')
        exam_result['page_no'] = pageNo
        if isSame:
            exam_result['score'] += exam_result['score']
        else:
            exam_result['score'] = 0

        # 若题号和题目数相等，则表示这是最后一题,还需要更新finish_time
        if pageNo == question_count:
            exam_result['finish_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 更新测试记录
        MpExamService_instance.update_by_id(id=exam_result['id'], data=exam_result)

    # 创建新的用户选项信息
    for optionId in optionIds:
        new_useroption = {
            "user_id": userId,
            "exam_id": examId,
            "is_duoxue": 1,
            "question_id": questionId,
            "option_id": optionId,
            "is_right": 1 if rightIds.__contains__({"option_id": optionId}) else 0,
        }
        # 新增新的用户选项记录
        MpOptionService_instance.add(new_useroption)

    return ResponseUtil.success()


"""
计算并获取测试结果
"""
@router.post("/result")
def result(userId = Body(None),examId = Body(None)):
    logger.info(f'/mp/exam/result, user_id = {userId}, exam_id = {examId}')

    # 查询用户最近一次完成的测试记录
    JsonArray = []
    last_finish_user_exam = MpUserExamService_instance.get_one_by_filters(filters={
        "user_id": userId,
        "exam_id": examId,
        "finish_time": True
    })
    if last_finish_user_exam is None:
        return ResponseUtil.error(data={"message": "用户未完成任何测试"})
    else:
        JsonArray.append({
            "user_exam_id": last_finish_user_exam['id'],
            "right_num": last_finish_user_exam['score'],
            "error_num": last_finish_user_exam['page_no']-last_finish_user_exam['score'],
        })

    ## 查询全部测试记录
    all_finish_user_exams = MpUserExamService_instance.get_list_by_filters(filters={
        "user_id": userId,
        "exam_id": examId,
        "finish_time": True
    })
    JsonArray2 = []
    for user_exam in all_finish_user_exams:
        JsonArray2.append({
            "sum_num": user_exam['page_no'],
            "right_num": user_exam['score'],
            "error_num": user_exam['page_no']-user_exam['score'],
            "time_num": user_exam['finish_time']
        })
    JsonArray.append(JsonArray2)

    return ResponseUtil.success(data=JsonArray)


"""
查询用户测试历史记录
"""
@router.post("/history")
def history(userId = Body(None,embed=True)):
    logger.info(f'/mp/exam/history, user_id = {userId}')
    JsonArray = []

    #查询该用户的全部测试历史记录
    all_finish_user_exams = MpUserExamService_instance.get_list_by_filters(filters={
        "user_id": userId,
        "finish_time": True
    })

    # 遍历所有测试记录，将其转换为json格式
    for user_exam in all_finish_user_exams:
        # 根据exam_id 查询对应的测试信息
        exam_info = MpExamService_instance.get_one_by_filters(filters={
            "id": user_exam['exam_id']
        })
        # 将历史测试记录转换为json格式，并添加到JsonArray中
        JsonArray.append({
            "examId": exam_info['exam_id'],
            "examName": exam_info['name'],
            "finishTime": user_exam['finish_time'],
        })

    return ResponseUtil.success(data=JsonArray)


"""
进行问题分析
"""
@router.post("/questionAnalyse")
def questionAnalyse(userId = Body(None),examId = Body(None)):
    logger.info(f'/mp/exam/questionAnalyse, user_id = {userId}, exam_id = {examId}')
    JsonArray = []

    # 获取最近一次的测试记录
    last_finish_user_exam = MpUserExamService_instance.get_one_by_filters(filters={
        "user_id": userId,
        "exam_id": examId,
        "finish_time": True
    })
    # 查询最近一次测试的问题列表
    last_question_list = MpQuestionService_instance.get_list_by_filters(filters={
        "exam_id": examId,
    })
    for question in last_question_list:
        json = {}
        json['questionId'] = question['id']
        qid = question['id']
        qtype = question['type']

        # 查询某个测试的某个问题的选项数据
        uOption = MpUserOptionService_instance.get_list_by_filters(filters={
            "user_exam_id": last_finish_user_exam['id'],
            "question_id": question['id'],
        })

        if qtype == "单选题":
            # 单选题
            if uOption[0]["is_right"] == 1:
                json['isAnswerCorrect'] = 1
            else:
                json['isAnswerCorrect'] = 0

        elif qtype == "多选题":
            # 多选题
            # 查询用户选择的选项集合
            choiceIds = []
            for u in uOption:
                choiceIds.append(u['option_id'])

            # 查询正确的选项集合
            rightIds = []
            right_items = MpOptionService_instance.get_list_by_filters(filters={
                "question_id": qid,
                "score": 1,
            })
            for r in right_items:
                rightIds.append(r['id'])

            # 将正确选项集合和用户选择的选项集合进行对比
            isSame:bool = False
            if set(choiceIds) == set(rightIds):
                isSame = True
            else:
                isSame = False

            # 根据对比结果判断用户是否回答正确
            if isSame:
                json['isAnswerCorrect'] = 1
            else:
                json['isAnswerCorrect'] = 0

        JsonArray.append(json)

    return ResponseUtil.success(data=JsonArray)


"""
选项分析
"""
@router.post("/optionAnalyse")
def optionAnalyse(userExamId = Body(None),questionId = Body(None)):
    logger.info(f'/mp/exam/optionAnalyse, user_exam_id = {userExamId}, question_id = {questionId}')
    JsonArray = []
    json = {}

    # 用户选择的选项id集合
    choiceNums = []

    # 查询用户选择的选项id集合
    choiceIds = []
    uoptions = MpUserOptionService_instance.get_list_by_filters(filters={
        "user_exam_id": userExamId,
        "question_id": questionId,
    })
    for u in uoptions:
        choiceIds.append(u['option_id'])

    # 根据question_id 查询问题内容
    question = MpQuestionService_instance.get_one_by_filters(filters={
        "id": questionId,
    })
    json['question_name'] = question['name']
    JsonArray.append(json)

    # 根据question_id 查询选项内容
    options = MpOptionService_instance.get_list_by_filters(filters={
        "question_id": questionId,
    })
    JsonArray2 = []
    num:int = 0
    for o in options:
        option_num:str = f"A{num}"
        json2 = {
            "option_num": option_num,
            "option_name": o['content'],
            "isRight": 1 if o['score'] > 1 else 0,
        }
        if choiceIds.__contains__(o['id']):
            choiceNums.append(option_num+"")

        JsonArray2.append(json2)
        num += 1

    JsonArray.append(JsonArray2)
    # 描述文本
    json3 = {
        "text":choiceNums.__dict__
    }
    JsonArray.append(json3)

    return ResponseUtil.success(data=JsonArray)




















