from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from sqlalchemy.orm import Session
from models.article import ArticleModel,ArticleCreate,Base
from lib.orm import get_db
router=APIRouter(prefix="/blog/article",tags=["Blog Article"])

# db=Database()

@router.post("/add")
async def article_create(data: ArticleCreate, db: Session = Depends(get_db)):
  # print(user)
  # creat table
  # Base.metadata.create_all(bind=db.bind)
  dbData=ArticleModel(**data.model_dump())
  db.add(dbData)
  db.commit() 
  db.refresh(dbData) 
  return dbData 


@router.get("/list")
async def article_list(db: Session = Depends(get_db)):
  list=db.query(ArticleModel).all()
  return list
