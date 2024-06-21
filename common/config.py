# 数据库url
from fastapi import HTTPException

db_url = "mysql://root:123456@114.116.253.17:3306/starbi"

TORTOISE_ORM = {
    # 连接信息
    "connections": {"default": db_url},
    "apps": {
        "models": {  # 这个models 表示应用名称作用就是你在使用到关联模型 {app}.{model} 这时候你的app 就叫models
            # model 信息
            # "models": ["models", "aerich.models"], # 把需要的模型导进一个module 直接使用module
            "models": ["models.user","models.knowledge"],  # 把需要的模型导进一个module 直接使用module
            "default_connection": "default",
        },
    },
}

# tortoise orm logging
import logging, sys

fmt = logging.Formatter(
    fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)

# will print debug sql
logger_db_client = logging.getLogger("tortoise.db_client")
logger_db_client.setLevel(logging.DEBUG)
logger_db_client.addHandler(sh)


class BusinessException(HTTPException):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
from fastapi.middleware.cors import CORSMiddleware

class CORSConfig:
    def __init__(self, app):
        self.app = app
        self.setup_cors()

    def setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )