from faker import Faker  # 用于生成虚假数据
import random  # 用于生成随机数据
from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from pydantic import BaseModel
from typing import Optional

import sys
sys.path.append("..")
from lib.database import dbconn

fake = Faker()  # 创建一个虚假数据生成器

def generate_test_data(data_length):
  conn = dbconn()
  cursor = conn.cursor()
  
  for _ in range(data_length):
      # 生成虚假数据
    userid = fake.user_name()
    alias = fake.name()
    mobile = fake.phone_number()
    email = fake.email()
    password = fake.password()
    role = random.randint(1, 4)  # 随机生成1到5之间的角色ID
    print(f"userid:{userid}, alias:{alias}, mobile:{mobile}, email:{email}, password:{password}, role:{role}")
    
    cursor.execute("INSERT INTO user (userid, alias, mobile, email, password, role, createdate) VALUES (%s, %s, %s, %s, %s, %s, NOW())", (userid, alias, mobile, email, password, role))
    conn.commit()
      
  cursor.close()
  conn.close()

generate_test_data(1)