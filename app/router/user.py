from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from sqlalchemy.orm import Session
from models.user import UserModel,UserCreate,Base
from lib.orm import get_db
router=APIRouter(prefix="/system/user",tags=["System User"])

# db=Database()

@router.post("/add")
async def user_create(data: UserCreate, db: Session = Depends(get_db)):
  # print(user)
  Base.metadata.create_all(bind=db.bind)
  dbData=UserModel(**data.model_dump())
  db.add(dbData)
  db.commit()  # 提交事务
  db.refresh(dbData)  # 刷新用户对象，以获取数据库中生成的主键等信息
  return dbData  # 返回创建的用户对象
  return dbData.name  # 返回创建的用户对象

@router.get("/list")
async def user_list(db: Session = Depends(get_db)):
  list=db.query(UserModel).all()
  for i in range(len(list)):
    print(list[i].name)
  return list
