from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from pydantic import BaseModel
from typing import Optional
import json
from lib.database import dbconn
from lib.jwtToken import check_jwt
router=APIRouter(prefix="/system/permission",tags=["System Permission"])


@router.post("/add",dependencies=[Depends(check_jwt)])
async def permission_add(
  role: int = Body(...),
  perm_menu: list[str] = Body(...),
  perm_operate: list[str] = Body(...),
  perm_origin: list[list[str]] = Body(...),
):
  
  perm_menu_json = json.dumps(perm_menu)
  perm_operate_json = json.dumps(perm_operate)
  perm_origin_json = json.dumps(perm_origin)
  
  conn=dbconn()
  cursor = conn.cursor()
  try:
    cursor.execute("INSERT INTO sys_permission (role,perm_menu,perm_operate,perm_origin) VALUES (%s, %s, %s, %s)", (role,perm_menu_json,perm_operate_json,perm_origin_json))
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
async def permission_edit(
  id: int = Body(...),
  role: int = Body(...),
  perm_menu: list[str] = Body(...),
  perm_operate: list[str] = Body(...),
  perm_origin: list[list[str]] = Body(...),
):
  
  perm_menu_json = json.dumps(perm_menu)
  perm_operate_json = json.dumps(perm_operate)
  perm_origin_json = json.dumps(perm_origin)
 
  conn = dbconn()
  cursor = conn.cursor()
  try:
    cursor.execute("SELECT id FROM sys_permission WHERE id = %s", (id,))
    existing_id = cursor.fetchone()

    if not existing_id:
      return {
        "success":False,
        "message":f"Menu with ID {id} not found"
      }
    cursor.execute("UPDATE sys_permission SET role = %s, perm_menu = %s, perm_operate = %s, perm_origin = %s WHERE id = %s", (
      role,perm_menu_json,perm_operate_json, perm_origin_json, id))
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




@router.delete("/delete",dependencies=[Depends(check_jwt)])
async def permission_delete(id: int):
  
  conn = dbconn()
  cursor = conn.cursor()

  try:
    cursor.execute("SELECT id FROM sys_permission WHERE id = %s", (id,))
    existing_id = cursor.fetchone()
    print(existing_id)
    if not existing_id:
      return {
        "success":False,
        "message":f"Menu with ID {id} not found"
      }
    cursor.execute("DELETE FROM sys_permission WHERE id = %s", (id,))
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



# process flat menu to tree
def build_menu(data, parent_id=0):
  menu = []
  boolean_fields = ["keepAlive", "hideInTab", "hideInNav", "isParent"]
  for item in data:
    if item["parent"] == parent_id:
      children = build_menu(data, item["id"])
      if children:
        item["children"] = children
      # 转换最后3个字段的值为True/False
      for field in boolean_fields:
        item[field] = item[field] == 1
      menu.append(item)
  return menu

def find_orphan_items(data):
  orphan_items = []
  for item in data:
    if item["parent"] != 0 and not any(parent["id"] == item["parent"] for parent in data):
      orphan_items.append(item)
  # print(orphan_items)
  return orphan_items



@router.get("/list",dependencies=[Depends(check_jwt)])
async def permission_list(
    query: Optional[str] = Query(None),
    pageSize: int = Query(10), 
    page: int = Query(1), 
):
  conn = dbconn()
  cursor = conn.cursor()
  try:
    sql = "SELECT * FROM sys_permission WHERE 1"
    params = []

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