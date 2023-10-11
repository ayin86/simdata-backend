from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from sqlalchemy import asc
from sqlalchemy.orm import Session
from models.article import ArticleModel,ArticleBase,QueryBase,Base
from lib.orm import get_db
router=APIRouter(prefix="/blog/article",tags=["Blog Article"])

# db=Database()

@router.post("/add")
async def article_create(data: ArticleBase, db: Session = Depends(get_db)):
  try:
    # print(user)
    # creat table
    Base.metadata.create_all(bind=db.bind)
    dbData=ArticleModel(**data.model_dump())
    db.add(dbData)
    db.commit() 
    db.refresh(dbData) 
    return {
      "success":True,
      "data":dbData
    }
  except Exception as e:
    raise HTTPException(status_code=502, detail=str(e))


# @router.get("/list")
# async def article_list(db: Session = Depends(get_db)):
#   list=db.query(ArticleModel).all()
#   return list


@router.get("/list")
async def article_list(params:QueryBase= Depends(), db: Session = Depends(get_db)):
  try:
    offset = (params.page-1) * params.pageSize
    list=db.query(ArticleModel).order_by(asc(ArticleModel.id)).offset(offset).limit(params.pageSize).all()
    total_records = db.query(ArticleModel).count()
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