from config.database_config import session_maker
from modules.module_exam.models.mp_exam_model import MpExamModel
from modules.module_exam.dto.mp_exam_dto import MpExamDTO

class MpExamDao:
    @classmethod
    def get_list(cls, pageSize: int, pageNum: int):
        with session_maker() as db_session:
            res = db_session.query(MpExamModel).limit([pageNum, pageSize]).all()
            print("result=", res)
            return res

    @classmethod
    def get_list_by(cls, dto: MpExamDTO):
        with session_maker() as db_session:
            res = db_session.query(MpExamModel).filter(MpExamModel.name == dto.name).all()
            return res

    @classmethod
    def update_by_id(cls, dto: MpExamDTO):
        # dict()方法可以将对象转换为字典类型数据
        with session_maker() as db_session:
            res = db_session.query(MpExamModel).filter(MpExamModel.id == dto.id).update(dto.dict())
            print("result=", res)
            return res

    @classmethod
    def delete_by_id(cls, dto: MpExamDTO):
        with session_maker() as db_session:
            res = db_session.query(MpExamModel).filter(MpExamModel.id == dto.userId).delete()
            print("result=", res)
            return res

    @classmethod
    def add(cls, dto: MpExamDTO):
        with session_maker() as db_session:
            one = MpExamModel(**dto)
            res = db_session.add(one)
            print("result=", res)
            return res