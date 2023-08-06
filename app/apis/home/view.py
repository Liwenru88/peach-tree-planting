from fastapi import APIRouter, Body

from app.schemas import ResponseSchema

home_router = APIRouter()


@home_router.post("/home_retrieve", summary="获取首页数据", response_model=ResponseSchema)
async def home_retrieve(
        keyword_type: int = Body(..., description="关键字类型"),
        keyword: str = Body(..., description="关键字"),
):
    """
    获取首页数据
    :return:
    """

    return ResponseSchema(data={})
