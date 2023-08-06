from fastapi import APIRouter

from app.schemas import ResponseSchema
from app.schemas.request_schema import CreateUserSchema

user_router = APIRouter()


# TODO 用户管理
@user_router.post("/create-user", summary="创建用户", response_model=ResponseSchema)
async def create_user(
    user_obj: CreateUserSchema
):
    """创建用户"""
    return ResponseSchema(data=user_obj.dict())


@user_router.get("/get-user-list", summary="获取用户列表", response_model=ResponseSchema)
async def get_user_list(
    page: int = 1,
    page_size: int = 10
):
    """获取用户列表"""

    data = [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@admin.com",
            "phone": "12345678901",
            "role_id": 1,
            "role_name": "管理员",
            "create_time": "2021-01-01 00:00:00",
            "update_time": "2021-01-01 00:00:00",
        },
        {
            "id": 2,
            "username": "user",
            "email": "user@user.com",
            "phone": "12345678901",
            "role_id": 2,
            "role_name": "普通用户",
            "create_time": "2021-01-01 00:00:00",
            "update_time": "2021-01-01 00:00:00",
        }
    ]

    return ResponseSchema(data=data, totalCount=2, currentPage=1)


@user_router.get("/get-user-info", summary="获取用户信息", response_model=ResponseSchema)
async def get_user_info(
    user_id: int
):
    """获取用户信息"""
    data = {
        "id": 1,
        "username": "admin",
        "email": "admin@admin.com",
        "phone": "12345678901",
        "role_id": 1,
        "role_name": "管理员",
        "create_time": "2021-01-01 00:00:00",
        "update_time": "2021-01-01 00:00:00",
    }
    return ResponseSchema(data=data)


@user_router.put("/update-user-info", summary="更新用户信息", response_model=ResponseSchema)
async def update_user_info():
    """更新用户信息"""
    return ResponseSchema(data={})

# TODO 权限管理
