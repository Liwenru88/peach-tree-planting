from fastapi import APIRouter, File, UploadFile, Body

from app.schemas import ResponseSchema
from app.schemas.request_schema import DataLabelingSchema

data_manage_router = APIRouter()


# TODO 资料上传和OCR识别
@data_manage_router.post("/upload-data", summary="资料上传")
async def upload_data(
        file: UploadFile = File(...),
):
    return ResponseSchema(data={"filename": file.filename})


# TODO 数据标注
@data_manage_router.post("/data-labeling", summary="数据标注")
async def data_labeling(
        data_labeling_obj: DataLabelingSchema
):
    return ResponseSchema(data={"result": "success"})


@data_manage_router.post("/add-category-label", summary="添加分类标签")
async def add_category_label(
        label_name: str = Body(..., embed=True, description="标签名称")
):
    """
    添加分类标签
    :param label_name:
    :return:
    """

    return ResponseSchema(data={"result": "success"})


@data_manage_router.get("/get-category-label", summary="获取分类标签")
async def get_category_label():
    """
    获取分类标签
    :return:
    """
    category_label_list = [
        {
            "label_id": 1,
            "label_name": "分类标签1"
        },
        {
            "label_id": 2,
            "label_name": "分类标签2"
        },
        {
            "label_id": 3,
            "label_name": "分类标签3"
        }
    ]

    return ResponseSchema(data=category_label_list)
