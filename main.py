from fastapi import FastAPI
import models
from database import engine
from routers import todo, user, auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router=todo.router)
app.include_router(router=user.router)
app.include_router(router=auth.router)

