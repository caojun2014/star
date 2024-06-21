from typing import Generic, T

from pydantic.v1.generics import GenericModel
from starlette.responses import JSONResponse


class BusinessException(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code

    @property
    def get_code(self):
        return self.code

from enum import Enum


class R(GenericModel, Generic[T]):
    code: int
    data: T
    msg: str

    @staticmethod
    def ok(msg: str = "success", data: T = None) -> "R":
        return R(code=200, msg=msg, data=data)

    @staticmethod
    def error(code = 400,msg: str = "fail", data: T = None) -> "R":
        return R(code=400, msg=msg, data=data)

    def error(code=400, msg: str = "fail", data: T = None) -> "R":
        return R(code=400, msg=msg, data=data)
