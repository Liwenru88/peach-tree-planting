from fastapi import APIRouter, Query

from app.schemas.request_schema import KnowledgeAdvancedSearch

knowledge_router = APIRouter()


@knowledge_router.post("/knowledge-advanced-search", summary="知识高级搜索")
async def knowledge_advanced_search(
        request_obj: KnowledgeAdvancedSearch,
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, description="每页数量")
):
    pass


@knowledge_router.get("/get-article-detail", summary="获取文章详情")
async def get_article_detail(
        article_id: str = Query(..., description="文章id")
):
    pass


@knowledge_router.get("/get-article-directory", summary="获取文章目录")
async def get_article_directory(
        article_id: str = Query(..., description="文章id")
):
    pass


@knowledge_router.get("/get-similar-article", summary="获取相似文章")
async def get_similar_article(
        article_id: str = Query(..., description="文章id")
):
    pass


@knowledge_router.get("/get-relevant-information", summary="获取相关资料")
async def get_relevant_information(
        article_id: str = Query(..., description="文章id")
):
    pass


@knowledge_router.get("/get-related-author-article", summary="获取相关作者文章")
async def get_related_author_article(
        article_id: str = Query(..., description="文章id")
):
    pass
