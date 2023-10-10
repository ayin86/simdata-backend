from fastapi import APIRouter,HTTPException,Request,Body,Header,Depends
from pydantic import BaseModel
from typing import Optional
from lib.database import dbconn
from lib.tools import process_password
from lib.jwtToken import enc_jwt,dec_jwt,get_token
from os import remove,makedirs,rmdir,listdir,stat
from os.path import join, exists,isfile, isdir
from lib.jwtToken import check_jwt

router=APIRouter(prefix="/account",tags=["Account"])

async def get_auth(authorization: str = Header(None)):
    if authorization is None:
      raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    return token

@router.put("/edit",dependencies=[Depends(check_jwt)])
async def account_update(
  token: str = Depends(get_auth),
  id: int = Body(...),
  userid: str = Body(...),
  username: str = Body(...),
  mobile: str = Body(...),
  email: str = Body(...),
  role: int = Body(...),
  avatar: Optional[str] = Body(None),
  country: Optional[str] = Body(None),
  language: Optional[str] = Body(None),
  site: Optional[str] = Body(None),
  github: Optional[str] = Body(None),
  intro: Optional[str] = Body(None),
):
  print(123)
  dec_token=dec_jwt(token)
  print(dec_token)
  conn = dbconn()
  cursor = conn.cursor()
  try:
    cursor.execute("SELECT id,avatar FROM sys_user WHERE id = %s", (id,))
    existing_id = cursor.fetchone()
    
    if avatar and avatar!=existing_id[1] and existing_id[1]!="avatar.jpeg":
      file_path="uploads\\avatar\\"+existing_id[1]
      if exists(file_path) and isfile(file_path):
          remove(file_path)
      # print(existing_id[1])
    if not existing_id:
      return {
        "success":False,
        "message":f"User with ID {id} not found"
      }
    cursor.execute("UPDATE sys_user SET userid= %s, username= %s, mobile= %s, email= %s, role= %s, avatar=%s, createdate=NOW(), country= %s, language= %s, site= %s, github= %s, intro= %s WHERE id = %s", (
      userid, username, mobile, email, role, avatar, country, language, site, github, intro, id))
    conn.commit()
    
    
    # 获取账户信息
    cursor.execute("SELECT * FROM sys_user WHERE userid = %s", (userid))
    user_data = cursor.fetchone()
    user_detail=dict(zip([column[0] for column in cursor.description], user_data))
    user_detail.pop("password")
    
    # 获取角色信息
    cursor.execute("SELECT * FROM sys_dict WHERE type = 'role' AND value = %s",(role))
    roleRows = cursor.fetchall()
    role_detail = [dict(zip([column[0] for column in cursor.description], row)) for row in roleRows]
    # print(user_detail)
    return {
      "success":True,
      "userInfo":{"userid":userid,"username":username,"token":dec_token["token"],"role":role_detail[0],"userDetail":user_detail},
    }
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=502, detail=str(e))
  finally:
    cursor.close()
    conn.close()


@router.put("/setpass",dependencies=[Depends(check_jwt)])
async def set_password(
  token: str = Depends(get_auth),
  original: str = Body(...),
  newpass: str = Body(...),
):
  dec_token=dec_jwt(token)
  userid=dec_token["payload"]["userid"]
  print(userid)
  conn = dbconn()
  cursor = conn.cursor()
  
  try:
    cursor.execute("SELECT * FROM sys_user WHERE userid = %s", (userid,))
    existing_id = cursor.fetchone()
    print(existing_id)
    
    oriPass_process=process_password(original)
    if existing_id[5]==oriPass_process:
      newPass_process=process_password(newpass)
      print(newPass_process)
      cursor.execute("UPDATE sys_user SET password= %s WHERE userid = %s", (newPass_process,userid))
      conn.commit()
      return {
        "success":True,
      }
    else:
      return {
        "success":False,
        "message":"Original password is incorrect !"
      }
  except Exception as e:
    raise HTTPException(status_code=502, detail=str(e))  # 保留502错误处理
  finally:
    cursor.close()
    conn.close()




@router.delete("/terminate",dependencies=[Depends(check_jwt)])
async def delete_account(id: int):
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
  