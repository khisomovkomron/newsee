from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(Model):
    
    id = fields.IntField(pk=True)
    email = fields.CharField(unique=True, index=True, max_length=100)
    username = fields.CharField(unique=True, index=True, max_length=100)
    first_name = fields.CharField(max_length=50, null=True)
    second_name = fields.CharField(max_length=50, null=True)
    hashed_password = fields.CharField(max_length=200)
    phone_number = fields.IntField(null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ["name"]
        
        
class Verification(Model):
    """ Модель для подтверждения регистрации пользователя
    """
    link = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.Users', related_name='verification')


user_pydantic = pydantic_model_creator(Users)
