# 导入sqlalchemy框架中的相关字段
from sqlalchemy import Column, Integer, String, DateTime, CHAR, func, Index
# 导入公共基类
from config.database_config import myBaseModel

class MpOptionModel(myBaseModel):
    """
    选项表 mp_option
    """
    __tablename__ = 'mp_option'

    id = Column("id",Integer, primary_key=True, autoincrement=True, comment='选项id')
    question_id = Column("question_id", Integer, nullable=False, comment='问题id')
    content = Column("content",String(500),nullable=False, comment='选项内容')
    score = Column("score",Integer,nullable=False, comment='选项分数，0为错误答案，1分正确答案')
    is_ban = Column("is_ban",Integer, default=0, comment='是否禁用 0正常 1停用')
    status = Column("status",Integer, default=0, comment='测试状态 0正常 1停用')
    create_time = Column("create_time",DateTime, comment='创建时间', default=func.now())

    # 添加索引
    __table_args__ = (
        Index('index_id', 'id'),
        Index('index_question_id', 'question_id'),
    )