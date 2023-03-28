from routers import user_news, users, auth, news, crypto, stocks, user_favorite_news
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from loguru import logger
from config.settings import DatabaseConfig, AppConfig
import uvicorn


app = FastAPI(
    title='NEWSEE',
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
app_config = AppConfig()

register_tortoise(
    app,
    db_url=database_config.databse_url,
    modules={'models': ['db.models', 'aerich.models']},
    generate_schemas=False,
    add_exception_handlers=True
)

if __name__ == "__main__":

    uvicorn.run(
        'main:app',
        host=app_config.server_host,
        port=app_config.server_port,
        reload=True)