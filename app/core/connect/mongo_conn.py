from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional

from app.models.user_db import gather_user_db_documents
from app.core.config import settings

mongo_client: Optional[MongoClient] = None


async def init_mongodb():
    """
    初始化MongoDB连接

    :return:
    """
    global mongo_client

    mongo_client = AsyncIOMotorClient(settings.MOTOR_URI)

    # 初始化 mt_prod库连接
    await init_beanie(
        database=getattr(mongo_client, settings.MONGODB_USER_DB_NAME),
        document_models=gather_user_db_documents()
    )

    print(f"MongoDB init address:{mongo_client.address},db_name:{settings.MONGODB_USER_DB_NAME}")

    # 初始化mt_admin库连接
    # await init_beanie(
    #     database=getattr(mongo_client, app.config.MONGODB_ADMIN_DB_NAME),
    #     document_models=gather_mt_admin_documents()
    # )


def close_mongo_client():
    if not mongo_client:
        return
    mongo_client.close()
