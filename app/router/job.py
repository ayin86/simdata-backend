from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from sqlalchemy import asc
from sqlalchemy.orm import Session
from models.job import JobModel,JobBase,QueryBase,Base
from lib.orm import get_db
from pydantic import BaseModel
router=APIRouter(prefix="/common/job",tags=["Common Job"])


@router.post("/add")
async def job_create(data: JobBase, db: Session = Depends(get_db)):
  try:
    # creat table
    Base.metadata.create_all(bind=db.bind)
    dbData=JobModel(**data.model_dump())
    db.add(dbData)
    db.commit() 
    db.refresh(dbData) 
    return {
      "success":True,
      "data":dbData
    }
  except Exception as e:
    raise HTTPException(status_code=502, detail=str(e))


@router.put("/edit")
async def job_edit(data: JobBase, db: Session = Depends(get_db)):
  try:
    print(data.id)
    existing_id = db.query(JobModel).filter(JobModel.id == data.id).first()
    if not existing_id:
      return {
        "success":False,
        "message":f"Job with ID {data.id} not found"
      }
    for key, value in data.model_dump().items():
      setattr(existing_id, key, value)
    db.commit()
    db.refresh(existing_id)
    return {
      "success":True,
      "data":existing_id
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))



@router.get("/list")
async def job_list(params:QueryBase= Depends(), db: Session = Depends(get_db)):
  try:
    offset = (params.page-1) * params.pageSize
    list=db.query(JobModel).order_by(asc(JobModel.id)).offset(offset).limit(params.pageSize).all()
    total_records = db.query(JobModel).count()
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