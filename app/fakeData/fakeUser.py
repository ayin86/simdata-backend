from faker import Faker
import random

import sys
sys.path.append("..")
from lib.orm import get_db
from models.user import UserModel,UserCreate,Base

fake = Faker()

def fakedata_create(data_length=1):
  db = next(get_db())
  Base.metadata.create_all(bind=db.bind)
  for _ in range(data_length):
    userid = fake.user_name()
    alias = fake.name()
    mobile = fake.phone_number()
    email = fake.email()
    password = fake.password()
    sex = fake.random_element(elements=("Male", "Female"))
    role = random.randint(1, 4)
    dbData=UserModel(userid=userid, alias=alias, mobile=mobile, email=email, password=password, sex=sex, role=role)
    db.add(dbData)
    
  db.commit()
  db.refresh(dbData)
  return dbData

# fakedata_create(50)