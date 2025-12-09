# 导入sqlalchemy框架中的相关字段
from sqlalchemy import Column, Integer, String ,DateTime,CHAR,func
# 导入sqlalchemy的Base类
from sqlalchemy.ext.declarative import declarative_base
# 创建基类Base
Base = declarative_base()

class MpOptionModel(Base):
    """
    选项表 mp_option
    """
    __tablename__ = 'mp_option'

    id = Column("id",Integer, primary_key=True, autoincrement=True, comment='选项id')
    question_id = Column("question_id", Integer, nullable=False, comment='问题id')
    content = Column("content",String(500),unique=True,nullable=False, comment='选项内容')
    score = Column("score",String(20),unique=True,nullable=False, comment='选项分数，0为错误答案，1分正确答案')
    isBan = Column("is_ban",CHAR(2), default='0', comment='是否禁用 0正常 1停用')
    status = Column("status",CHAR(2), default='0', comment='测试状态 0正常 1停用')
    create_time = Column("create_time",DateTime, comment='创建时间', default=func.now())
