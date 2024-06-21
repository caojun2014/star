import logging
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Depends, HTTPException,Request
from fastapi_sessions.frontends.implementations import SessionCookie

from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, PlainTextResponse
from tortoise.contrib.fastapi import register_tortoise

from common.config import TORTOISE_ORM, BusinessException, CORSConfig
from router.user import user_router
from router.files import file_router
from router.knowledge import  knowledge_router
app = FastAPI(title="mini-rbac")
from starlette.middleware.sessions import SessionMiddleware
from common.utils.ResponseRes import R
register_tortoise(app, config=TORTOISE_ORM)
app.add_middleware(SessionMiddleware, secret_key="caojun")
# 跨域


app.include_router(file_router)
app.include_router(user_router)
app.include_router(knowledge_router)

## 自定义异常
app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logging.error("参数错误", exc_info=exc)
    return R.error(code = 500, msg = "参数错误")

@app.exception_handler(BusinessException)
async def handle_business_exception(request, exc: BusinessException):
    logging.error("BusinessException", exc_info=exc)
    return JSONResponse(
        status_code=400,
        content={
            "code":400,
            "message": str(exc.message)}
    )

    #return PlainTextResponse(str(exc.message), status_code=exc.status_code)



# 中间件

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.options("/{proxy+}")
async def options_handler():
    return {}
@app.middleware("http")
async def handle_options(request: Request, call_next):
    if request.method == "OPTIONS":
        return {}
    return await call_next(request)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)