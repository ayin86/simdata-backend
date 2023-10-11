from fastapi import Query
from sqlalchemy import Column, Integer, String,Text, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
import datetime
# from typing import Optional

Base = declarative_base()

class ArticleModel(Base):
  __tablename__ = "article"
  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(50), unique=True, nullable=False)
  content = Column(Text)
  author = Column(String(20))
  read_count = Column(Integer)
  like_count = Column(Integer)
  dislike_count = Column(Integer)
  createdate = Column(DateTime,default=datetime.datetime.utcnow())
  
  # def __init__(self):
  #   self.createdate = datetime.datetime.utcnow()
    
class ArticleBase(BaseModel):
  # id:int = None
  title:str
  content: str
  author: str
  read_count: int
  like_count: int
  dislike_count: int
  # createdate: str = None

class QueryBase(BaseModel):
  page: int = Query(1, description="Page number", ge=0)
  pageSize: int = Query(10, description="Number of items per page", ge=1)