# 导入sqlalchemy框架中的相关字段
from sqlalchemy import Column, Integer, String ,DateTime,CHAR,func
# 导入sqlalchemy的Base类
from sqlalchemy.ext.declarative import declarative_base
# 创建基类Base
Base = declarative_base()

class MpUserOptionModel(Base):
    """
    用户选项表 mp_user_option
    """
    __tablename__ = 'mp_user_option'

    id = Column("id",Integer, primary_key=True, autoincrement=True, comment='用户选项id')
    userId = Column("user_id", Integer, nullable=False, comment='用户id')
    examId = Column("exam_id", Integer, nullable=False, comment='测试id')
    userExamId = Column("user_exam_id", Integer, nullable=False, comment='用户测试id')
    optionId = Column("option_id", Integer, nullable=False, comment='选项id')
    questionId = Column("question_id", Integer, nullable=False, comment='问题id')
    isDuoxue = Column("is_duoxue", Integer, nullable=False, comment='是否多选,0为否，1为是')
    isRight = Column("is_right", Integer, nullable=False, comment='是否正确,0为否，1为是')
    createTime = Column("create_time",DateTime, comment='创建时间', default=func.now())
