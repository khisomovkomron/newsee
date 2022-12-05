from typing import Optional

from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    phone_number: Optional[str] | None = None


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description='The priority must be between 1-5')
    complete: bool


class Archive(BaseModel):
    title: str
    status: bool


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str
    apt_num: Optional[int]


class Profile(BaseModel):
    user: CreateUser
    address: Address
    todo: Todo


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str
