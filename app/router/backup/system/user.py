from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from pydantic import BaseModel
from typing import Optional, Dict,Any
from lib.database import dbconn
from lib.tools import process_password
from lib.jwtToken import check_jwt
router=APIRouter(prefix="/system/user",tags=["System User"])


@router.post("/add",dependencies=[Depends(check_jwt)])
async def add_user(
  userid: str = Body(...),
  username: str = Body(...),
  mobile: str = Body(...),
  email: str = Body(...),
  password: str = Body(...),
  role:int = Body(...),
):
  conn=dbconn()
  cursor = conn.cursor()
  newPass=process_password(password)
  try:
    cursor.execute("SELECT COUNT(*) FROM sys_user")
    data_length = cursor.fetchone()[0]
    cursor.execute("ALTER TABLE sys_user AUTO_INCREMENT = %s",(data_length + 1))
    conn.commit()
    
    cursor.execute("INSERT INTO sys_user (userid, username, mobile, email, password,role, createdate) VALUES (%s, %s, %s, %s, %s, %s, NOW())", (userid, username, mobile, email, newPass, role))
    conn.commit()
    return {
      "success":True,
      "userid":userid,
      "username":username
    }
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=502, detail=str(e))
  finally:
    cursor.close()
    conn.close()
  




@router.put("/edit",dependencies=[Depends(check_jwt)])
async def user_edit(
  id: int = Body(...),
  userid: str = Body(...),
  username: str = Body(...),
  mobile: str = Body(...),
  email: str = Body(...),
  password: str = Body(...),
  role:int = Body(...),
):
  newPass=process_password(password)
  conn = dbconn()
  cursor = conn.cursor()
  try:
    cursor.execute("SELECT id FROM sys_user WHERE id = %s", (id,))
    existing_id = cursor.fetchone()

    if not existing_id:
      return {
        "success":False,
        "message":f"User with ID {id} not found"
      }
    cursor.execute("UPDATE sys_user SET userid= %s, username= %s, mobile= %s, email= %s, password= %s, role= %s, createdate=NOW() WHERE id = %s", (
      userid, username, mobile, email, newPass, role, id))
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
async def user_list(
    role: Optional[int] = Query(None),
    query: Optional[str] = Query(None),
    page: int = Query(1, description="页码，从1开始"),
    pageSize: int = Query(10, description="每页记录数")
) -> Dict[str, Any]:
  conn = dbconn()
  cursor = conn.cursor()
  try:
    sql = "SELECT * FROM sys_user WHERE 1"
    params = []

    if role is not None:
      sql += " AND role = %s"
      params.append(role)

    if query:
      sql += " AND (userid LIKE %s OR username LIKE %s OR email LIKE %s)"
      params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])

    count_sql = f"SELECT COUNT(*) FROM sys_user WHERE 1 {'AND role = %s' if role is not None else ''} {'AND (userid LIKE %s OR username LIKE %s OR email LIKE %s)' if query else ''}"
    cursor.execute(count_sql, params)
    total_records = cursor.fetchone()[0]

    offset = (page - 1) * pageSize
    sql += f" LIMIT %s OFFSET %s"
    params.extend([pageSize, offset])

    cursor.execute(sql, params)

    rows = cursor.fetchall()
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    total_pages = (total_records + pageSize - 1) // pageSize

    return {
      "success":True,
      "data": result,
      "totalRecords": total_records,
      "totalPages": total_pages,
      "currentPage": page,
      "pageSize": pageSize
    }
      
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=500, detail=str(e))
  finally:
    cursor.close()
    conn.close()


@router.delete("/delete",dependencies=[Depends(check_jwt)])
async def user_delete(id: int):
  conn = dbconn()
  cursor = conn.cursor()

  try:
    cursor.execute("SELECT id FROM sys_user WHERE id = %s", (id,))
    existing_id = cursor.fetchone()
    print(existing_id)
    if not existing_id:
      return {
        "success":False,
        "message":f"User with ID {id} not found"
      }
    cursor.execute("DELETE FROM sys_user WHERE id = %s", (id,))
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