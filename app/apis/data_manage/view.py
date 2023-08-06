from fastapi import APIRouter, File, UploadFile

from app.schemas import ResponseSchema

data_manage_router = APIRouter()


# TODO 资料上传和OCR识别
@data_manage_router.post("/upload-data", summary="资料上传")
async def upload_data(
        file: UploadFile = File(...),
):
    return ResponseSchema(data={"filename": file.filename})


# TODO 数据标注
@data_manage_router.post("/data-labeling", summary="数据标注")
async def data_labeling():
    pass


@data_manage_router.post("/add-category-label", summary="添加分类标签")
async def add_category_label():
    pass


@data_manage_router.get("/get-category-label", summary="获取分类标签")
async def get_category_label():
    pass
