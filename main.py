from routers import todo, user, auth, address
from database import engine
from fastapi import FastAPI
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router=todo.router)
app.include_router(router=user.router)
app.include_router(router=auth.router)
app.include_router(router=address.router)

