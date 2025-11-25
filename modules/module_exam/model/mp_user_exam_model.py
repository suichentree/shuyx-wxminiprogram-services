# 导入sqlalchemy框架中的相关字段
from sqlalchemy import Column, Integer, String ,DateTime,CHAR,func
# 导入sqlalchemy的Base类
from sqlalchemy.ext.declarative import declarative_base
# 创建基类Base
Base = declarative_base()

class MpUserExamModel(Base):
    """
    用户测试表 mp_user_exam
    """
    __tablename__ = 'mp_user_exam'

    id = Column("id",Integer, primary_key=True, autoincrement=True, comment='用户测试id')
    userId = Column("user_id", Integer, nullable=False, comment='用户id')
    examId = Column("exam_id", Integer, nullable=False, comment='测试id')
    pageNo = Column("page_no", Integer, nullable=False, comment='当前页码')
    score = Column("score", Integer, nullable=False, comment='用户测试分数')
    createTime = Column("create_time",DateTime, comment='创建时间', default=func.now())
    finishTime = Column("finish_time", DateTime, comment='测试完成时间')
