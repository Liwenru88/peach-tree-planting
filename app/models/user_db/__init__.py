import sys
from beanie import Document
from app.models.user_db.user_model import User


def gather_user_db_documents():
    """
    获取 `models` 模块中定义的所有 MongoDB 文档模型的列表。
    :return:
    """
    from inspect import getmembers, isclass

    return [
        doc
        for _, doc in getmembers(sys.modules[__name__], isclass)
        if issubclass(doc, Document) and doc.__name__ != "Document"
    ]
