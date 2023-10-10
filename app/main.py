import uvicorn
from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

# from router.base import router as router_base
# from router.profile import router as router_profile
# from router.register import router as router_register

# from router.docs import router as router_docs
# from router.auth import router as router_auth
# from router.system.menu import router as router_system_menu
# from router.system.dict import router as router_system_dict
# from router.system.user import router as router_system_user
# from router.system.permission import router as router_system_permission

# from router.blog.article import router as router_blog_article
# from router.blog.comment import router as router_blog_comment
# from router.blog.likeDislike import router as router_blog_likeDislike
# from router.attachment.file import router as router_file
# from router.account import router as router_account


app = FastAPI(docs_url=None, redoc_url=None)


comPath="/api"

# app.include_router(router_docs)
# app.include_router(router_auth, prefix=comPath)
# app.include_router(router_account, prefix=comPath)
# app.include_router(router_file, prefix=comPath)
# app.include_router(router_blog_likeDislike, prefix=comPath)
# app.include_router(router_blog_comment, prefix=comPath)
# app.include_router(router_blog_article, prefix=comPath)



# app.include_router(router_system_menu, prefix=comPath)
# app.include_router(router_system_dict, prefix=comPath)
# app.include_router(router_system_user, prefix=comPath)
# app.include_router(router_system_permission, prefix=comPath)

# app.include_router(router_base, prefix=comPath)
# app.include_router(router_profile, prefix=comPath)
# app.include_router(router_register, prefix=comPath)

app.mount('/static', StaticFiles(directory='../static'))
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


if __name__=="__main__":
  uvicorn.run("main:app",reload=True)
  # uvicorn.run(app) 