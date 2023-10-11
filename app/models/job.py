from fastapi import Query
from sqlalchemy import Column, Integer, String,Text, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
import datetime
# from typing import Optional

Base = declarative_base()

class JobModel(Base):
  __tablename__ = "job"
  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(50), nullable=False)
  company = Column(String(50))
  type = Column(String(100))
  skills = Column(String(100))
  education = Column(String(100))
  salary_min = Column(Integer)
  salary_max = Column(Integer)
  contact_info = Column(String(100))
  deadline = Column(DateTime)
  description = Column(Text)
  
    
class JobBase(BaseModel):
  id: int = None 
  title: str
  company: str
  type: str
  skills: str
  education: str = None
  salary_min: int
  salary_max: int
  contact_info: str
  deadline: str
  description: str = None


class QueryBase(BaseModel):
  page: int = Query(1, description="Page number", ge=0)
  pageSize: int = Query(10, description="Number of items per page", ge=1)
