from faker import Faker
import random
from datetime import datetime, timedelta

import sys
sys.path.append("..")
from lib.orm import get_db
from models.job import JobModel,Base

fake = Faker()

def fakedata_create(data_length=1):
  db = next(get_db())
  Base.metadata.create_all(bind=db.bind)
  for _ in range(data_length):
    title = fake.job()
    company = fake.company()
    job_type = fake.job()
    skills = fake.words(nb=5) 
    education = fake.random_element(elements=("High School", "Bachelor's", "Master's", "PhD"))
    salary_min = random.randint(30000, 80000)
    salary_max = random.randint(60000, 120000)
    contact_info = fake.email()
    deadline = datetime.now() + timedelta(days=random.randint(7, 30))
    description = fake.paragraph(nb_sentences=3)

    dbData = JobModel(
        title=title,
        company=company,
        type=job_type,
        skills=",".join(skills),  # 将技能列表转换为逗号分隔的字符串
        education=education,
        salary_min=salary_min,
        salary_max=salary_max,
        contact_info=contact_info,
        deadline=deadline,
        description=description
    )
    db.add(dbData)
    
  db.commit()
  db.refresh(dbData)
  return dbData

fakedata_create(10)