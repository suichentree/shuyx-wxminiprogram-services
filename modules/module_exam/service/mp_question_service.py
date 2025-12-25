from typing import List, Dict, Any

from .base_service import BaseService
from ..dao.mp_option_dao import MpOptionDao
from ..dao.mp_question_dao import MpQuestionDao
from ..dto.mp_option_dto import MpOptionDTO
from ..dto.mp_question_dto import MpQuestionDTO, MpQuestionOptionDTO
from ..model.mp_option_model import MpOptionModel
from ..model.mp_question_model import MpQuestionModel

class MpQuestionService(BaseService[MpQuestionModel, MpQuestionDTO]):
    """
    继承自通用服务基类  提供相关的业务逻辑处理
    """

    def __init__(self):
        """
        初始化服务实例
        创建DAO实例并传递给基类
        """
        dao_instance = MpQuestionDao()
        super().__init__(dao_instance)
        # 创建选项DAO实例用于转换
        self.option_dao = MpOptionDao()

    # 可以根据业务需求添加自定义方法

    def get_questions_with_options(self, exam_id: int) -> List[MpQuestionOptionDTO]:
        """
        获取指定测试的所有问题及其选项
        """
        # 使用session_execute_query方法执行JOIN查询
        result = self.session_execute_query(
            lambda db_session: db_session.query(
                MpQuestionModel,
                MpOptionModel
            ).join(
                MpOptionModel,
                MpQuestionModel.id == MpOptionModel.question_id
            ).filter(
                MpQuestionModel.exam_id == exam_id,
                MpQuestionModel.status == 0
            ).all()
        )

        # 处理查询结果，将选项分组到对应的问题中
        question_dict: Dict[int, Dict[str, Any]] = {}

        # 遍历结果
        for question_model, option_model in result:
            # 如果问题已经在字典中，只需要添加选项
            if question_model.id in question_dict:
                existing_question = question_dict[question_model.id]
                if option_model:  # 如果有选项
                    option_dict = self.option_dao._model_to_dict__(option_model)
                    existing_question["options"].append(option_dict)
            else:
                # 创建新的问题项并添加到字典中
                question_dict[question_model.id] = {
                    **self.dao._model_to_dict__(question_model),
                    "options": []
                }
                if option_model:  # 如果有选项
                    option_dict = self.option_dao._model_to_dict__(option_model)
                    question_dict[question_model.id]["options"].append(option_dict)

        # 将字典转换为复合DTO列表并返回
        return [
            MpQuestionOptionDTO.model_validate(question_dict)
            for question_dict in question_dict.values()
        ]

