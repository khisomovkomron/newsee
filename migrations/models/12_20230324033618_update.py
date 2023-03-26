from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "usernews" ADD "user_id" INT NOT NULL;
        ALTER TABLE "usernews" ADD CONSTRAINT "fk_usernews_users_28a9a6f5" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "usernews" DROP CONSTRAINT "fk_usernews_users_28a9a6f5";
        ALTER TABLE "usernews" DROP COLUMN "user_id";"""
