from fastapi import APIRouter,FastAPI,Depends, File,Form, UploadFile,Request,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from os import remove,makedirs,rmdir,listdir,stat
from os.path import join, exists,isfile, isdir
from datetime import datetime
from typing import Optional,List
import time 
import uuid
from PIL import Image
from lib.jwtToken import check_jwt

router=APIRouter(prefix="/attachment/file",tags=["Attachment File"])

@router.post("/upload",dependencies=[Depends(check_jwt)])
async def upload_files(
  request: Request,
  files: List[UploadFile], 
  path: Optional[str] = Form(None),
  extension: Optional[str] = Form(None),
  rename: Optional[str] = Form(None),
):
  try:
    file_urls = [] 
    
    for file in files:
      if path is None:
        storage_path = "uploads"
      else:
        storage_path = join("uploads", path)
      if not exists(storage_path):
        makedirs(storage_path)
      
      timestamp = int(time.time() * 1000)
      file_extension = file.filename.split('.')[-1] 
      print(file.filename)
      shortUUID = str(uuid.uuid4()).split('-')[-1]
      if rename:
        if len(files)==1:
          filename = f"{rename}-{shortUUID}.{file_extension}"
        else:
          filename = f"{rename}-{timestamp}-{shortUUID}.{file_extension}"
      else:
        filename = f"{timestamp}-{shortUUID}.{file_extension}"
      
      file_path = join(storage_path, filename)
      
      with open(file_path, "wb") as f:
        f.write(file.file.read())
      
      if file_extension.lower() in ['png', 'jpeg', 'jpg', 'bmp']:
        ext_replace = [".bmp", ".png"]
        new_file_path = file_path
        for ext in ext_replace:
            new_file_path = new_file_path.replace(ext, ".jpeg")
        
        image = Image.open(file_path)
        
        if path == 'avatar':
          image = image.resize((128, 128))
          
        image.thumbnail((1280, 1280))
        image = image.convert("RGB")
        image.save(new_file_path, format="JPEG", quality=80)
        
        if file_extension.lower() not in {'jpg', 'jpeg'}:
          if exists(file_path) and isfile(file_path):
            remove(file_path)
          
        file_urls.append("/"+new_file_path.replace("\\","/"))
      else:
        file_urls.append("/"+file_path.replace("\\","/"))
     
      # file_url = f"/uploads/{path}/{filename}" if path is not None else f"/uploads/{filename}"
      # file_urls.append(file_url)
      
    return {
      "urls": file_urls,
      "success":True
    }
  except Exception as e:
    raise HTTPException(status_code=502, detail=str(e))


def get_file_info(path,item):
    return {
      "fullName": item,
      "name": item.split(".")[0],
      "extension": item.split(".")[-1],
      "size": stat(join(path,item)).st_size,
      "path": path,
      "uploadDate": datetime.fromtimestamp(stat(path).st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    }

@router.get("/list",dependencies=[Depends(check_jwt)])
async def list_files(
  page: int = Query(default=1, description="page number"),
  pageSize: int = Query(default=10, description="number per page"),
  path: str = Query(default=None, description="Fuzzy matching path"),
  name: str = Query(default=None, description="Fuzzy matching name"),
  extension: str = Query(default=None, description="Fuzzy matching extension")
):
  try:
    root_dir = "uploads"
    if not exists(root_dir) or not isdir(root_dir):
      return {
        "success":False,
        "message":"Root directory does not exist !"
      }
    file_info_list = []

    def process_directory(dir_path):
      for item in listdir(dir_path):
        item_path = join(dir_path, item)
        if isfile(item_path):
          file_info = get_file_info(dir_path, item)
          if (
            (path is None or path in file_info["path"]) and
            (name is None or name in file_info["name"]) and
            (extension is None or extension in file_info["extension"])
          ):file_info_list.append(file_info)
        elif isdir(item_path):
          process_directory(item_path)

    process_directory(root_dir)

    total_records = len(file_info_list)
    total_pages = (total_records + pageSize - 1) // pageSize

    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize
    paginated_data = file_info_list[start_index:end_index]

    return {
      "success":True,
      "currentPage": page,
      "data": paginated_data,
      "pageSize": pageSize,
      "totalPages": total_pages,
      "totalRecords": total_records
    }
  except Exception as e:
    raise HTTPException(status_code=502, detail=str(e))


@router.delete("/delete",dependencies=[Depends(check_jwt)])
async def delete_file(
  path: str = Query(..., description="File path"), 
  name: str = Query(..., description="File name")
):
  try:
    file_path = join(path, name)
    if exists(file_path) and isfile(file_path):
      remove(file_path)
      if not listdir(path) and path != "uploads":
        rmdir(path)
      return {
        "success":True,
        "message": f"File {name} was successfully deleted."
      }
    else:
      return {
        "success":False,
        "message":f"File {name} does not exist or cannot be deleted."
      }
  except Exception as e:
    raise HTTPException(status_code=502, detail=str(e))