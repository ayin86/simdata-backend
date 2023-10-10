from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from pydantic import BaseModel
from typing import Optional
from lib.database import dbconn
from lib.menu import build_menu,find_orphan_items
from lib.jwtToken import check_jwt
router=APIRouter(prefix="/system/menu",tags=["System Menu"])


@router.post("/add",dependencies=[Depends(check_jwt)])
async def menu_add(
  id: int = Body(...),
  parent: int = Body(...),
  icon: str = Body(...),
  label: str = Body(...),
  title: str = Body(...),
  path: str = Body(...),
  operate: list[int] = Body(...),
  keepAlive: bool = Body(...),
  hideInTab: bool = Body(...),
  hideInNav: bool = Body(...),
  isParent: bool = Body(...),
  enable: bool = Body(...),
):
  operate_str = ",".join(map(str, operate))
  
  conn=dbconn()
  cursor = conn.cursor()
  try:
    cursor.execute("INSERT INTO sys_menu (id,parent,icon,label,title,path,operate,keepAlive,hideInTab,hideInNav,isParent,enable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id,parent,icon,label,title,path,operate_str,keepAlive,hideInTab,hideInNav,isParent,enable))
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
async def menu_edit(
  id: int = Body(...),
  parent: int = Body(...),
  icon: str = Body(...),
  label: str = Body(...),
  title: str = Body(...),
  path: str = Body(...),
  operate: list[int] = Body(...),
  keepAlive: bool = Body(...),
  hideInTab: bool = Body(...),
  hideInNav: bool = Body(...),
  isParent: bool = Body(...),
  enable: bool = Body(...),
):
  operate_str = ",".join(map(str, operate))
  
  conn = dbconn()
  cursor = conn.cursor()
  try:
    cursor.execute("SELECT id FROM sys_menu WHERE id = %s", (id,))
    existing_id = cursor.fetchone()

    if not existing_id:
      return {
        "success":False,
        "message":f"Menu with ID {id} not found"
      }
    cursor.execute("UPDATE sys_menu SET parent = %s, icon = %s, label = %s, title = %s, path = %s, operate = %s, keepAlive = %s, hideInTab = %s, hideInNav = %s, isParent=%s, enable=%s WHERE id = %s", (
      parent, icon, label, title, path, operate_str, keepAlive, hideInTab, hideInNav, isParent, enable, id))
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
async def menu_delete(id: int):
  
  conn = dbconn()
  cursor = conn.cursor()

  try:
    cursor.execute("SELECT id FROM sys_menu WHERE id = %s", (id,))
    existing_id = cursor.fetchone()
    print(existing_id)
    if not existing_id:
      return {
        "success":False,
        "message":f"Menu with ID {id} not found"
      }
    cursor.execute("DELETE FROM sys_menu WHERE id = %s", (id,))
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
async def menu_list(query: str = Query(None)):
  conn = dbconn()
  cursor = conn.cursor()
  try:
    if query:
      # 使用模糊查询来过滤数据
      cursor.execute("SELECT * FROM sys_menu WHERE label LIKE %s OR title LIKE %s", (f"%{query}%", f"%{query}%"))
    else:
      cursor.execute("SELECT * FROM sys_menu")
    
    rows = cursor.fetchall()
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    tree_menu = build_menu(result)
    orphan_menu=find_orphan_items(result)
    tree_menu.extend(orphan_menu)
    return {
      "success":True,
      "menu":tree_menu
    }
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=500, detail=str(e))
  finally:
    cursor.close()
    conn.close()