from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.BigIntField(pk=True, generated=True, description='id')
    userAccount = fields.CharField(max_length=256, description='账号')
    userPassword = fields.CharField(max_length=512, description='密码')
    userName = fields.CharField(max_length=256, null=True, description='用户昵称')
    userAvatar = fields.CharField(max_length=1024, null=True, description='用户头像')
    userRole = fields.CharField(max_length=256, default='user', description='用户角色：user/admin')
    createTime = fields.DatetimeField(auto_now_add=True, description='创建时间')
    updateTime = fields.DatetimeField(auto_now=True, description='更新时间')
    isDelete = fields.BooleanField(default=False, description='是否删除')

    class Meta:
        table = 'user'
        table_description = '用户'


UserPydantic = pydantic_model_creator(User, name='User')
