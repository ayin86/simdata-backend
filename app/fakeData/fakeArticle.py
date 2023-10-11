from faker import Faker
import random
from datetime import datetime, timedelta

import sys
sys.path.append("..")
from lib.orm import get_db
from models.article import ArticleModel,Base

fake = Faker()

def fakedata_create(data_length=1):
  db = next(get_db())
  Base.metadata.create_all(bind=db.bind)
  for _ in range(data_length):
    title = fake.catch_phrase()
    content = fake.paragraphs(nb=3)  # 生成3段文章内容
    author = fake.name()
    read_count = random.randint(100, 10000)
    like_count = random.randint(10, 1000)
    dislike_count = random.randint(1, 100)
    createdate = datetime.now() - timedelta(days=random.randint(1, 365))

    dbData = ArticleModel(
        title=title,
        content="\n".join(content),  # 将段落列表合并为文章内容
        author=author,
        read_count=read_count,
        like_count=like_count,
        dislike_count=dislike_count,
        createdate=createdate
    )
    db.add(dbData)
    
  db.commit()
  db.refresh(dbData)
  return dbData

fakedata_create(10)