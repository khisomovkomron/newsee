from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "usernews" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "title" VARCHAR(200),
    "description" TEXT,
    "link_to_news" TEXT,
    "image_url" TEXT,
    "content" TEXT,
    "language" VARCHAR(50),
    "creator" TEXT
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "usernews";"""
