import uvicorn
from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from router.docs import router as router_docs
from router.user import router as router_user
from router.job import router as router_job
from router.article import router as router_article

app = FastAPI(docs_url=None, redoc_url=None)
comPath="/simdata"

app.include_router(router_article, prefix=comPath)
app.include_router(router_user, prefix=comPath)
app.include_router(router_job, prefix=comPath)
app.include_router(router_docs)


app.mount('/static', StaticFiles(directory='../static'))
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
if __name__=="__main__":
  uvicorn.run("main:app",reload=True)
  uvicorn.run(app) 