from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Test(Base):
    __tablename__ = "test1"  # 테이블 이름 정의

    # 테이블의 열을 정의
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    confirm = Column(Boolean, default=True)
