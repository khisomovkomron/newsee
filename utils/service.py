from typing import Optional

from tortoise.expressions import Q

from utils.auth_helpers import *

from db import schemas, models
from .service_base import BaseService
from tortoise.contrib.pydantic import pydantic_model_creator


class UserService(BaseService):
    model = models.Users
    create_schema = pydantic_model_creator(models.Users)
    get_schema = schemas.user_get_pydantic

    async def create_user(self, schema):
        hash_password = get_hashed_password(schema.dict().pop("password"))
        obj = await self.model.create(**schema.dict(exclude={"password"}), hashed_password=hash_password)
        res = await self.create_schema.from_tortoise_orm(obj)
        return res
        

    async def authenticate(self, username: str, password: str) -> Optional[models.Users]:
        user = await self.model.get(username=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def change_password(self, obj: models.Users, new_password: str):
        hashed_password = get_hashed_password(new_password)
        obj.password = hashed_password
        await obj.save()

    async def create_user_social(self, user: schemas.CreateUser):
        return await self.create_user(schema=user, is_active=True)

    async def get_username_email(self, username: str, email: str):
        return await self.model.get_or_none(Q(username=username) | Q(email=email))


user_s = UserService()