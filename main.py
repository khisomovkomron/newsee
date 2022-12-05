from routers import todo, \
    user, \
    auth, \
    address, \
    profile, \
    archive
from database_pack.database import engine
from database_pack import models
from fastapi import FastAPI

app = FastAPI(
    title='TODO LEARNING PROJECT',
    description='project based on FastApi using different tools that were learnt everyday during this campagne'
)

models.Base.metadata.create_all(bind=engine)

app.include_router(router=auth.router)
app.include_router(router=user.router)
app.include_router(router=profile.router)
app.include_router(router=todo.router)
app.include_router(router=address.router)
app.include_router(router=archive.router)

