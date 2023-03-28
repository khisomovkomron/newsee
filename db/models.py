from tortoise import models, fields


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
        ordering = ["created_at"]


class News(models.Model):

    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=200, null=True)
    description = fields.TextField(null=True)
    content = fields.TextField(null=True)
    link_to_news = fields.TextField(null=True)
    creator = fields.TextField(null=True)
    language = fields.CharField(max_length=50, null=True)
    country = fields.CharField(max_length=50, null=True)
    category = fields.CharField(max_length=50, null=True)
    image_url = fields.TextField(null=True)
    datetime = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["datetime"]


class UserNews(models.Model):

    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=200, null=True)
    description = fields.TextField(null=True)
    link_to_news = fields.TextField(null=True)
    image_url = fields.TextField(null=True)
    content = fields.TextField(null=True)
    language = fields.CharField(max_length=50, null=True)
    creator = fields.TextField(null=True)
    user = fields.ForeignKeyField(model_name='models.Users', related_name='user_news')
    user_comment = fields.TextField(null=True)

    class Meta:
        ordering = ["id"]
