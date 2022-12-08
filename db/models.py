from tortoise import models
from tortoise import fields


class Users(models.Model):
    
    id = fields.IntField(pk=True)
    username = fields.CharField(unique=True, index=True, max_length=100)
    email = fields.CharField(unique=True, index=True, max_length=100)
    first_name = fields.CharField(max_length=50, null=True)
    second_name = fields.CharField(max_length=50, null=True)
    hashed_password = fields.CharField(max_length=200)
    phone_number = fields.IntField(null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ["username"]


