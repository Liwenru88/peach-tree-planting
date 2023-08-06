from fastapi import APIRouter

from app.apis.login.view import login_router
from app.apis.user.view import user_router
from app.apis.home.view import home_router
from app.apis.knowledge_manage.view import knowledge_router
from app.apis.data_manage.view import data_manage_router

api_router = APIRouter()
api_router.include_router(login_router, prefix="/login", tags=["登录接口"])
api_router.include_router(user_router, prefix="/user", tags=["用户接口"])
api_router.include_router(home_router, prefix="/home", tags=["首页接口"])
api_router.include_router(knowledge_router, prefix="/knowledge", tags=["知识管理接口"])
api_router.include_router(data_manage_router, prefix="/data_manage", tags=["数据管理接口"])
