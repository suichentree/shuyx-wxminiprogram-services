# 导入sqlalchemy框架中的相关字段
from sqlalchemy import Column, Integer, String ,DateTime,CHAR,func
# 导入sqlalchemy的Base类
from sqlalchemy.ext.declarative import declarative_base
# 创建基类Base
Base = declarative_base()

class MpQuestionModel(Base):
    """
    问题表 mp_question
    """
    __tablename__ = 'mp_question'

    id = Column("id",Integer, primary_key=True, autoincrement=True, comment='问题id')
    examId = Column("exam_id", Integer, nullable=False, comment='测试id')
    name = Column("name",String(255),unique=True,nullable=False, comment='问题名称')
    type = Column("type",String(20),unique=True,nullable=False, comment='问题类型')
    typeId = Column("type_id", Integer, nullable=False, comment='问题类型id,1为单选，2为多选')
    isBan = Column("is_ban",Integer, default=0, comment='是否禁用 0正常 1停用')
    status = Column("status",Integer, default=0, comment='测试状态 0正常 1停用')
    createTime = Column("create_time",DateTime, comment='创建时间', default=func.now())
