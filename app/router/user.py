from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from sqlalchemy.orm import Session
from sqlalchemy import asc
from models.user import UserModel,UserBase,QueryBase,Base
from lib.orm import get_db
router=APIRouter(prefix="/system/user",tags=["System User"])

# db=Database()

@router.post("/add")
async def user_create(data: UserBase, db: Session = Depends(get_db)):
  try:
    # print(user)
    Base.metadata.create_all(bind=db.bind)
    dbData=UserModel(**data.model_dump())
    db.add(dbData)
    db.commit()  # 提交事务
    db.refresh(dbData)  # 刷新用户对象，以获取数据库中生成的主键等信息
    return {
      "success":True,
      "data":dbData
    }
    # return dbData.name
  except Exception as e:
    raise HTTPException(status_code=502, detail=str(e))

# @router.get("/list")
# async def user_list(db: Session = Depends(get_db)):
#   list=db.query(UserModel).all()
#   for i in range(len(list)):
#     print(list[i].name)
#   return list


@router.get("/list")
async def user_list(params:QueryBase= Depends(), db: Session = Depends(get_db)):
  try:
    offset = (params.page-1) * params.pageSize
    list=db.query(UserModel).order_by(asc(UserModel.id)).offset(offset).limit(params.pageSize).all()
    total_records = db.query(UserModel).count()
    total_pages = (total_records + params.pageSize - 1) // params.pageSize
    return {
      "success":True,
      "totalRecords": total_records,
      "totalPages": total_pages,
      "currentPage": params.page,
      "pageSize": params.pageSize,
      "data": list
    }
  except Exception as e:
    raise HTTPException(status_code=502, detail=str(e))
