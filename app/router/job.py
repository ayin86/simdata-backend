from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from sqlalchemy.orm import Session
from models.job import JobModel,JobCreate,Base
from lib.orm import get_db
router=APIRouter(prefix="/common/job",tags=["Common Job"])

# db=Database()

@router.post("/add")
async def article_create(data: JobCreate, db: Session = Depends(get_db)):
  # creat table
  Base.metadata.create_all(bind=db.bind)
  dbData=JobModel(**data.model_dump())
  db.add(dbData)
  db.commit() 
  db.refresh(dbData) 
  return dbData 


@router.get("/list")
async def article_list(db: Session = Depends(get_db)):
  list=db.query(JobModel).all()
  return list
