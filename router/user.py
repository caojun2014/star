from fastapi import APIRouter
from pydantic import BaseModel

from common.config import BusinessException
from common.utils.ResponseRes import R
from fastapi.requests import Request
from enity.dto.request_user import UserRegisterRequest
from models.user import User
from jwt.exceptions import InvalidTokenError

user_router = APIRouter(prefix="/api/user", tags=["用户管理"])


@user_router.get("/list", summary="获取用户列表")
async def get_users():
    return R.ok(data=await User.all())


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import bcrypt


@user_router.post("/register", summary="注册用户")
async def register_user(body: UserRegisterRequest | None):
    if body is None:
        raise BusinessException(400, "参数不能为空")
    userAccount = body.userAccount
    user_password = body.userPassword
    checkPassword = body.checkPassword
    if user_password != checkPassword:
        raise BusinessException(400, "两次密码不一致")
    user = await User.filter(userAccount=userAccount).first()
    if user:
        raise BusinessException(400, "用户已存在")

    # 使用 bcrypt 对密码进行加密
    hashed_password = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())
    await User.create(userAccount=userAccount, userPassword=hashed_password.decode())
    return R.ok(msg="注册成功")

class UserLoginRequest(BaseModel):
    userAccount: str
    userPassword: str


@user_router.post("/login", summary="登录")
async def login_user(user_login_request: UserLoginRequest, request: Request):
    if not user_login_request:
        raise BusinessException(400, "参数错误")

    user_account = user_login_request.userAccount
    user_password = user_login_request.userPassword

    if not user_account or not user_password:
        raise BusinessException(400, "参数错误")

    login_user_vo = await User.get(userAccount=user_account)

    # 使用 bcrypt 验证密码
    if bcrypt.checkpw(user_password.encode(), login_user_vo.userPassword.encode()):
        request.session["user_login"] = login_user_vo.id
        return R.ok(msg="登录成功")
    else:
        raise BusinessException(400, "用户名或密码错误")

@user_router.get("/get/login", summary="获取当前登录用户")
async def get_login_user(request: Request):
    if "user_login" in request.session:
        user_info = request.session["user_login"]
        return R.ok(data=user_info)
    else:
            raise BusinessException(401, "未登录")