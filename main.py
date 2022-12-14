from routers import user, auth, news
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config import settings
from loguru import logger


app = FastAPI(
    title='NEWSEE',
    description='A Platform for all news that you see'
)


app.include_router(router=auth.router)
app.include_router(router=user.router)
app.include_router(router=news.router)

logger.info('    RUNNING main.py')


register_tortoise(
    app,
    db_url="postgres://postgres:123abcDEF@localhost/NewseeDatabase",
    modules={'modules': settings.APPS_MODELS},
    generate_schemas=False,
    add_exception_handlers=True
)
