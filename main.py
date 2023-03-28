from application.stocks import stocks
from application.news import news
from application.crypto import crypto
from application.auth import auth
from application.user import user_news, users, user_favorite_news

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from loguru import logger
from config.settings import DatabaseConfig, AppConfig
import uvicorn

app_config = AppConfig()


app = FastAPI(
    title=app_config.project_name,
    description='A Platform for all news that you see'
)


app.include_router(router=auth.router)
app.include_router(router=users.router)
app.include_router(router=user_news.router)
app.include_router(router=user_favorite_news.router)
app.include_router(router=news.router)
app.include_router(router=crypto.router)
app.include_router(router=stocks.router)

logger.info('    RUNNING main.py')

database_config = DatabaseConfig()

register_tortoise(
    app,
    db_url=database_config.database_url,
    modules={'models': ['db.models', 'aerich.models']},
    generate_schemas=False,
    add_exception_handlers=True
)

if __name__ == "__main__":

    uvicorn.run(
        'src.main:app',
        host=app_config.server_host,
        port=app_config.server_port,
        reload=True)