from fastapi import APIRouter,Path,HTTPException,Header,Depends,Body

import random
from lib.registerModels import UserSignUp
import hashlib
import base64
import datetime
import json

from lib.jwtToken import enc_jwt,dec_jwt,get_token,oauth2_scheme
from lib.database import dbconn
from lib.menu import build_menu
from lib.tools import process_password
from lib.userInfo import assemble_user_info


code=""
router=APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/login",summary="login")
def login(
  userid:str=Body(...),
  password:str=Body(...),      
  captcha:str=Body(...)           
):
  newPass=process_password(password)
  try:
    print("captcha",code.lower(),"-",captcha.lower())
    if code.lower()!=captcha.lower():
      return {
        "success":False,
        "message":"Captcha code is wrong !"
      }
    
    user_info=assemble_user_info(userid,newPass)
    print(user_info)
    if user_info:
      return user_info
    else:
      return {
        "success":False,
        "message":"Wrong user name or password !"
      }
    # print(user_data,userid,newPass)
    # print(str(datetime.datetime.utcnow() + datetime.timedelta(hours=1)))
    # print(type(user_data))
    
  except Exception as e:
    raise HTTPException(status_code=502,detail=str(e))


# dec=dec_jwt()
# print("JWT Token:", token)
# print("dec:", dec)




@router.post("/register",summary="register")
def signup(form_data:UserSignUp=Body(...)):
  username=form_data.username
  password=form_data.password
  return {"name":username,"password":password}


from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
def generate_code(length=4):
  code = ""
  for _ in range(length):
    code += random.choice("ABCDEFGHJKLMNPRSTWXYZabcdefhkmnpqrstwxyz2345678")
  print(code)
  return code

def create_captcha_image(code):
  image = Image.new("RGB", (120, 60), (255, 255, 255))
  draw = ImageDraw.Draw(image)
  # font = ImageFont.truetype('./fonts/Triad.ttf', 35)
  font = ImageFont.truetype('./fonts/SirQuitry.ttf', 28)

  for x in range(30):
    for y in range(15):
      draw.point((x * 5, y * 5), fill=(0, 0, 0))
  draw.text((10, 15), code, fill=(0, 0, 0), font=font)
  return image

from captcha.image import ImageCaptcha
@router.get("/captcha")
async def get_captcha():
  global code
  try:
    code = generate_code()
    image = create_captcha_image(code)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    # image.write(code, 'uploads\captcha.png')
    return {
      "success":True,
      "image": "data:image/png;base64,"+image_base64
      # "code": code,
    }
  except Exception as e:
    raise HTTPException(status_code=502,detail=str(e))


# @router.post("/token")
# async def authorize(
#   username:str=Body(...),
#   password:str=Body(...),      
#   grant_type:str=Body(...)     
# ):
#   print(password,grant_type)
#   return {"token": username}


from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token", response_model=Token,)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
  try:
    userid = form_data.username
    password = form_data.password
    # newPass=process_password(password)
    print(password)
    login_info=assemble_user_info(userid,password)
    if login_info:
      print(login_info["userInfo"]["token"])   
      access_token = login_info["userInfo"]["token"]
      token_type = "bearer"
      return {"access_token": access_token, "token_type": token_type}
    else:
      raise Exception("Login failed!")
    
  except Exception as e:
    raise HTTPException(status_code=401,detail=str(e))



# @router.get("/protected-data")
# async def get_protected_data(data: str = Depends(oauth2_scheme)):
#     try:
#         print(data)
#         # Your code here
#         return {"token": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal Server Error")







# from captcha.image import ImageCaptcha
# @router.get("/captcha")
# async def get_captcha():
#   global code
#   try:
#     code = generate_code()
#     image = ImageCaptcha(
#       fonts=['./fonts/MKZodnigSquare.ttf'],
#       width=100, 
#       height=50,
#     )

#     data = image.generate(code)
#     # image.write(code, 'uploads\captcha.png')
#     base64_data = base64.b64encode(data.read()).decode('utf-8')
#     return {
#       "success":True,
#       "image": "data:image/png;base64,"+base64_data
#       # "code": code,
#     }
#   except Exception as e:
#     raise HTTPException(status_code=502,detail=str(e))

