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
  type = Column(String(20))
  skills = Column(String(100))
  education = Column(String(20))
  salary_min = Column(Integer)
  salary_max = Column(Integer)
  contact_info = Column(String(100))
  deadline = Column(DateTime)
  description = Column(Text)
  
    
class JobCreate(BaseModel):
  title: str
  company: str
  type: str
  skills: str
  education: str
  salary_min: int
  salary_max: int
  contact_info: str
  deadline: str
  description: str
