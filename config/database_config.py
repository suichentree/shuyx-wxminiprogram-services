# 导入pymysql模块
import pymysql
pymysql.install_as_MySQLdb()
# 导入sqlalchemy框架中的各个工具
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# mysql数据库的连接URL
MYSQL_DATABASE_URL = "mysql+pymysql://root:123456@localhost:33306/shuyx_db"

# 创建数据库引擎myEngine
myEngine = create_engine(MYSQL_DATABASE_URL,
    pool_size=5,            # 连接池大小
    pool_timeout=30,        # 池中没有线程最多等待的时间，否则报错
    echo=False              # 是否在控制台打印相关语句等
    )

# 创建统一基类
myBaseModel = declarative_base()

# 创建会话对象mySession
mySession = sessionmaker(autocommit=False, autoflush=False, bind=myEngine)

# 使用上下文模块，封装session,实现session的自动提交，自动回滚，自动关闭
@contextmanager
def session_maker(session=mySession()):
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()