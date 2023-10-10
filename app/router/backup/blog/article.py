from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body,Query
from pydantic import BaseModel
from typing import Optional, Dict,Any
from lib.database import dbconn
from lib.jwtToken import check_jwt
router=APIRouter(prefix="/blog/article",tags=["Blog Article"])

@router.post("/add",dependencies=[Depends(check_jwt)])
async def article_add(
  title: str = Body(...),
  content: str = Body(...),
  author: str = Body(...),
  topic: int = Body(...),
  state: int = Body(...),
):
  conn=dbconn()
  cursor = conn.cursor()
  try:
    cursor.execute("SELECT id FROM sys_user WHERE userid = %s", (author,))
    user_id = cursor.fetchone()
  
    cursor.execute("INSERT INTO blog_article (title, content, author, topic, state, createdate) VALUES (%s, %s, %s, %s, %s, NOW())", (title, content, user_id[0], topic, state))
    conn.commit()
    return {
      "success":True,
      "title": title, 
      "author": author
    }
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=502, detail=str(e))
  finally:
    cursor.close()
    conn.close()
  

@router.put("/edit",dependencies=[Depends(check_jwt)])
async def article_edit(
  id: int = Body(...),
  title: str = Body(...),
  content: str = Body(...),
  author: str = Body(...),
  topic: int = Body(...),
  state: int = Body(...),
):
  conn = dbconn()
  cursor = conn.cursor()
  try:
    cursor.execute("SELECT id FROM blog_article WHERE id = %s", (id,))
    existing_id = cursor.fetchone()
    
    cursor.execute("SELECT id FROM sys_user WHERE userid = %s", (author,))
    user_id = cursor.fetchone()

    if not existing_id:
      return {
        "success":False,
        "message":f"Menu with ID {id} not found"
      }
    cursor.execute("UPDATE blog_article SET title = %s, content = %s, author = %s, topic = %s, state=%s, updated = NOW() WHERE id = %s", (
      title, content, user_id[0], topic, state, id))
    conn.commit()
    return {
      "success":True,
      "title": title, 
      "author": author
    }
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=502, detail=str(e))
  finally:
    cursor.close()
    conn.close()

  
# @router.get("/list")
@router.get("/list",dependencies=[Depends(check_jwt)])
async def article_list(
  # token: str = Depends(oauth2_scheme),
  state: Optional[int] = Query(None),
  topic: Optional[int] = Query(None),
  query: Optional[str] = Query(None),
  page: int = Query(1, description="页码，从1开始"),
  pageSize: int = Query(10, description="每页记录数")
) -> Dict[str, Any]:
  
  # print("token",token)
  # if not verify_token(token):
  #   raise HTTPException(status_code=401, detail="Invalid token")
  conn = dbconn()
  cursor = conn.cursor()
  try:

    sql = """
      SELECT * FROM blog_article
      WHERE (%s IS NULL OR state = %s)
      AND (%s IS NULL OR topic = %s)
      AND (%s IS NULL OR (content LIKE %s OR title LIKE %s))
      LIMIT %s OFFSET %s
    """
    
    count_sql = """
      SELECT COUNT(*) FROM blog_article
      WHERE (%s IS NULL OR state = %s)
      AND (%s IS NULL OR topic = %s)
      AND (%s IS NULL OR (content LIKE %s OR title LIKE %s))
    """
    
    params = [state, state, topic, topic, query, f"%{query}%", f"%{query}%", pageSize, (page - 1) * pageSize]
    paramsCount = [state, state, topic, topic, query, f"%{query}%", f"%{query}%"]

    cursor.execute(count_sql, paramsCount)
    total_records = cursor.fetchone()[0]
    cursor.execute(sql, params)

    result = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    author_ids = {row["author"] for row in result if "author" in row}
    if author_ids:
      author_sql = "SELECT id, userid FROM sys_user WHERE id IN %s"
      cursor.execute(author_sql, (tuple(author_ids),))
      author_data = cursor.fetchall()

      author_id_to_userid = {row[0]: row[1] for row in author_data}

      for row in result:
        if "author" in row:
          author_id = row["author"]
          if author_id in author_id_to_userid:
            row["author_name"] = author_id_to_userid[author_id]

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
    raise HTTPException(status_code=502, detail=str(e))
  finally:
    cursor.close()
    conn.close()


@router.delete("/delete",dependencies=[Depends(check_jwt)])
async def article_delete(id: int):
  conn = dbconn()
  cursor = conn.cursor()

  try:
    cursor.execute("SELECT id FROM blog_article WHERE id = %s", (id,))
    existing_id = cursor.fetchone()
    if not existing_id:
      return {
        "success":False,
        "message":f"Article with ID {id} not found"
      }
    cursor.execute("DELETE FROM blog_article WHERE id = %s", (id,))
    conn.commit()
    return {
      "success":True
    }
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=502, detail=str(e))
  finally:
    cursor.close()
    conn.close()
  