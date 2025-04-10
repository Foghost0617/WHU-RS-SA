# # backend/database.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
#
# DB_URL = "mysql+mysqlconnector://root:118211yao@localhost/map_manager"
# engine = create_engine(DB_URL, echo=True)
# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
#
# # 数据库连接配置
# DB_URL = "mysql+mysqlconnector://root:118211yao@localhost/map_manager"
# engine = create_engine(DB_URL, echo=False)
# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()
#
# # 初始化数据库
# def init_db():
#     from models.tables import Base  # 延迟导入避免循环引用
#     Base.metadata.create_all(engine)

# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import json
import os
"""连接sql"""

# 获取 config2sql.json 的路径（兼容调试和 .exe 模式）
def get_config_path():
    # 打包后的 exe 运行目录
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_dir, "config2sql.json")

# 读取配置文件
with open(get_config_path(), "r", encoding="utf-8") as f:
    config = json.load(f)

# 构造数据库连接 URL
DB_URL = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset=utf8mb4"

# 创建引擎
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

