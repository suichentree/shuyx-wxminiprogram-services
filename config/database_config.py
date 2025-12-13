# 导入pymysql模块
import pymysql
pymysql.install_as_MySQLdb()
# 导入sqlalchemy框架中的各个工具
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# mysql数据库的连接URL
MYSQL_DATABASE_URL = "mysql+pymysql://root:123456@localhost:33306/shuyx_db"

# 创建数据库引擎myEngine
myEngine = create_engine(MYSQL_DATABASE_URL,
    pool_size=5,            # 连接池大小
    pool_timeout=30,        # 池中没有线程最多等待的时间，否则报错
    echo=False              # 是否在控制台打印相关语句等
    )

# 创建统一基类
class myBaseModel(DeclarativeBase):
    pass

# 创建会话对象mySession
mySession = sessionmaker(autocommit=False, autoflush=False, bind=myEngine, expire_on_commit=False)

# 使用上下文模块，封装session,实现session的自动提交，自动回滚，自动关闭
# 该函数用于创建新的会话对象，确保每个请求都有独立的会话。从而避免了并发访问同一个会话对象导致的事务冲突
@contextmanager
def session_maker():
    session = mySession()  # 每次都创建新的会话对象
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()