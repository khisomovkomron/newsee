from fastapi import FastAPI
import models
from database import engine
from routers import todo

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router=todo.router)
