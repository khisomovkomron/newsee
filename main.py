from routers import user, auth
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(
    title='NEWSEE',
    description='A Platform for all news that you see'
)


app.include_router(router=auth.router)
app.include_router(router=user.router)

register_tortoise(
    app,
    db_url="postgresql://postgres:123abcDEF@localhost/NewseeDatabase",
    modules={'modules': ["database_pack.models", "aerich.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)