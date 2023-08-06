from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class LabelingInfoSchema(BaseModel):
    """标注信息Schema"""
    category_labels: Optional[List[str]] = Field(None, description="分类标签列表", title="category_labels")
    title: Optional[str] = Field(None, description="标题", title="title")
    summary: Optional[str] = Field(None, description="摘要", title="summary")
    authors: Optional[List[str]] = Field(None, description="作者列表", title="authors")
    keywords: Optional[List[str]] = Field(None, description="关键词列表", title="keywords")
    literature_source: Optional[str] = Field(None, description="文献来源", title="literature_source")
    experimental_materials_list: Optional[List[str]] = Field(None, description="实验材料列表",
                                                             title="experimental_materials_list")
    article_number: Optional[str] = Field(None, description="文章编号", title="article_number")
    publication_date: Optional[datetime] = Field(None, description="发表日期", title="publication_date")
