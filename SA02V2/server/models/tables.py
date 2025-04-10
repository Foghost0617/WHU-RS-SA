from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String(100), unique=True, nullable=False)
    name = Column(String(100))
    password = Column(String(255), nullable=False)
# 地图表
class Map(Base):
    __tablename__ = "maps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    medium_type = Column(String(50))
    usage_type = Column(String(50))
    release_time = Column(Date)
    added_time = Column(TIMESTAMP, server_default=func.now())
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String(255))

# 地图日志表
class MapLog(Base):
    __tablename__ = "map_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    map_id = Column(Integer, ForeignKey("maps.id"))
    action = Column(String(50))  # add, update, delete
    action_time = Column(TIMESTAMP, server_default=func.now())


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    added_time = Column(TIMESTAMP, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    map_id = Column(Integer, ForeignKey("maps.id"))