from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "news" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "title" VARCHAR(200),
    "description" TEXT,
    "content" TEXT,
    "link_to_news" TEXT,
    "creator" TEXT,
    "language" VARCHAR(50),
    "country" VARCHAR(50),
    "category" VARCHAR(50),
    "image_url" TEXT,
    "datetime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "news";"""
