# 导入sqlalchemy框架中的相关字段
from sqlalchemy import Column, Integer, String ,DateTime,CHAR,func
# 导入sqlalchemy的Base类
from sqlalchemy.ext.declarative import declarative_base
# 创建基类Base
Base = declarative_base()

class MpUserModel(Base):
    """
    用户表 mp_user
    """
    __tablename__ = 'mp_user'

    id = Column("id",Integer, primary_key=True, autoincrement=True, comment='用户id')
    name = Column("name",String(500),unique=True,nullable=False, comment='用户名')
    password = Column("password",String(500),unique=True,nullable=False, comment='用户密码')
    phone = Column("phone", String(20), unique=True, nullable=False, comment='用户手机号')
    wxOpenId = Column("wx_openid", String(500), unique=True, nullable=False, comment='用户微信openid')
    wxUnionId = Column("wx_unionid", String(500), unique=True, nullable=False, comment='用户微信unionid')
    headUrl = Column("head_url", String(500), unique=True, nullable=False, comment='用户头像url')
    age = Column("age", Integer, nullable=False, comment='用户年龄')
    address = Column("address", String(500), unique=True, nullable=False, comment='用户地址')
    gender = Column("gender", Integer, nullable=False, comment='用户性别,0为暂无 1为男，2为女')
    email = Column("email", String(500), unique=True, nullable=False, comment='用户邮箱')
    loginCount = Column("login_count", Integer, nullable=False, comment='登录次数')
    lastLoginTime = Column("last_login_time", DateTime, comment='最后登录时间')
    isAdmin = Column("is_admin", Integer, nullable=False, comment='是否管理员,0为否，1为是')
    createTime = Column("create_time",DateTime, comment='创建时间', default=func.now())
