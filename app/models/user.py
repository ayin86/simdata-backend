from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
import datetime
# from typing import Optional

Base = declarative_base()

class UserModel(Base):
  __tablename__ = "user"
  # id: Mapped[int] = mapped_column(primary_key=True)
  # username: Mapped[str] = mapped_column(type_=String(255),unique=True)
  id = Column(Integer, primary_key=True, autoincrement=True)
  userid = Column(String(30), unique=True, nullable=False)
  alias = Column(String(30), unique=True, nullable=False)
  email = Column(String(30))
  mobile = Column(String(30))
  password = Column(String(20))
  role = Column(String(20))
  sex = Column(String(10),nullable=True)
  createdate = Column(DateTime,default=datetime.datetime.utcnow())
  
class UserCreate(BaseModel):
  userid: str
  alias: str
  email: str
  mobile: str
  password: str
  role: str
  sex: str
