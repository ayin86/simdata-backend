from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from pydantic import BaseModel
from typing import Optional
from lib.database import dbconn
from lib.jwtToken import check_jwt

router=APIRouter(prefix="/system/dict",tags=["System Dict"])

@router.post("/add",dependencies=[Depends(check_jwt)])
async def dict_add(
  name: str = Body(...),
  value:int =Body(...),
  bindto:str =Body(...),
  type:str =Body(...),
  description: str = Body(...),
):
  conn=dbconn()
  cursor = conn.cursor()
  try:
    cursor.execute("SELECT COUNT(*) FROM sys_dict")
    data_length = cursor.fetchone()[0]
    cursor.execute("ALTER TABLE sys_dict AUTO_INCREMENT = %s",(data_length + 1))
    conn.commit()
    
    cursor.execute("INSERT INTO sys_dict (name,value,bindto,type,description) VALUES (%s,%s,%s,%s,%s)", (name,value,bindto,type,description))
    conn.commit()
    return {
      "success":True,
    }
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=502, detail=str(e))
  finally:
    cursor.close()
    conn.close()




@router.put("/edit",dependencies=[Depends(check_jwt)])
async def dict_edit(
  id: int = Body(...),
  name: str = Body(...),
  value:int =Body(...),
  bindto:str =Body(...),
  type:str =Body(...),
  description: str = Body(...),
):
  conn = dbconn()
  cursor = conn.cursor()
  try:
    cursor.execute("SELECT id FROM sys_dict WHERE id = %s", (id,))
    existing_id = cursor.fetchone()

    if not existing_id:
      return {
        "success":False,
        "message":f"Dict with ID {id} not found"
      }
    cursor.execute("UPDATE sys_dict SET name= %s,description= %s, value=%s, bindto=%s, type=%s WHERE id = %s", (
      name, description, value, bindto, type, id))
    conn.commit()
    return {
      "success":True,
    }
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=502, detail=str(e))
  finally:
    cursor.close()
    conn.close()





@router.get("/list",dependencies=[Depends(check_jwt)])
async def dict_list(
  type: Optional[str] = Query(None),
  query: Optional[str] = Query(None),
  pageSize: int = Query(10), 
  page: int = Query(1), 
):
  conn = dbconn()
  cursor = conn.cursor()
  try:
    sql = "SELECT * FROM sys_dict WHERE 1"
    params = []

    if type:
        sql += " AND type = %s"
        params.append(type)

    if query:
        sql += " AND (name LIKE %s OR bindto LIKE %s OR description LIKE %s)"
        params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])

    cursor.execute(sql, params)
    total_count = cursor.rowcount

    total_pages = (total_count + pageSize - 1) // pageSize
    offset = (page - 1) * pageSize
    sql += f" LIMIT {pageSize} OFFSET {offset}"

    cursor.execute(sql, params)

    rows = cursor.fetchall()
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    
    return {
      "success":True,
      "data": result,
      "totalRecords": total_count,
      "totalPages": total_pages,
      "currentPage": page,
      "page_size": pageSize,
    }

  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=500, detail=str(e))
  finally:
    cursor.close()
    conn.close()


@router.delete("/delete",dependencies=[Depends(check_jwt)])
async def dict_delete(id: int):
  
  conn = dbconn()
  cursor = conn.cursor()

  try:
    cursor.execute("SELECT id FROM sys_dict WHERE id = %s", (id,))
    existing_id = cursor.fetchone()
    print(existing_id)
    if not existing_id:
      return {
        "success":False,
        "message":f"Dict with ID {id} not found"
      }
    cursor.execute("DELETE FROM sys_dict WHERE id = %s", (id,))
    conn.commit()
    return {
      "success":True,
    }
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=502, detail=str(e))
  finally:
    cursor.close()
    conn.close()


