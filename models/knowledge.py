from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class KnowledgeBase(models.Model):
    id = fields.BigIntField(pk=True)
    userID = fields.BigIntField()
    description = fields.TextField(null=True)
    OSSlink = fields.CharField(max_length=255, null=True)
    title = fields.CharField(max_length=255)
    createTime = fields.DatetimeField(auto_now_add=True)
    isDelete = fields.BooleanField(default=False)
    updateTime = fields.DatetimeField(auto_now=True)
    isProcessed = fields.BooleanField(default=False)

    class Meta:
        table = "KnowledgeBase"
        unique_together = (("id", "is_processed"),)


# 创建 Pydantic 模型以便于数据验证和序列化
KnowledgeBase_Pydantic = pydantic_model_creator(KnowledgeBase, name="KnowledgeBase")
KnowledgeBaseIn_Pydantic = pydantic_model_creator(KnowledgeBase, name="KnowledgeBaseIn", exclude_readonly=True)
