from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# データベースのORMモデルを定義
Base = declarative_base()

# AttendanceDBの内容定義
class AttendanceDB(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    number = Column(String(10), nullable=False)
    name = Column(String(50), nullable=False)
    grade = Column(String(10), nullable=False)
    date = Column(DateTime, nullable=False)

# NameDBの内容定義
class NameDB(Base):
    __tablename__ = 'name'
    id = Column(Integer, primary_key=True)
    number = Column(String(10), nullable=False)
    name = Column(String(50), nullable=False)
    grade = Column(String(10), nullable=False)

# SQLiteデータベースに接続
engine1 = create_engine('sqlite:///attendance.db')
engine2 = create_engine('sqlite:///name.db')

# データベースを作成
Base.metadata.create_all(engine1)
Base.metadata.create_all(engine2)