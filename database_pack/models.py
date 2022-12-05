from tortoise.models import Model
from tortoise import fields


class Users(Model):
    
    id = fields.IntField(pk=True)
    email = fields.CharField(unique=True, index=True, max_length=100)
    username = fields.CharField(unique=True, index=True, max_length=100)
    first_name = fields.CharField(max_length=50)
    second_name = fields.CharField(max_length=50)
    hashed_password = fields.CharField(max_length=200)
    phone_number = fields.IntField()
    is_active = fields.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    