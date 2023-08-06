from fastapi import APIRouter

login_router = APIRouter()


# TODO 登录管理
@login_router.get("/login-access-token", summary="获取登录token")
async def login_access_token():
    pass


