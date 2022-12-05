from routers import user, auth

from database_pack import models
from fastapi import FastAPI

app = FastAPI(
    title='NEWSEE',
    description='A Platform for all news that you see'
)


app.include_router(router=auth.router)
app.include_router(router=user.router)
