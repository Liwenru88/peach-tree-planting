from typing import Dict, List, Union
from enum import Enum

from pydantic import BaseModel, Field


class KnowledgeAdvancedSearch(BaseModel):
    """知识高级搜索Schema"""
    and_type_list: List[Dict] = Field(..., description="and类型列表", title="and_type_list")
    or_type_list: List[Dict] = Field(..., description="or类型列表", title="or_type_list")
    not_type_list: List[Dict] = Field(..., description="not类型列表", title="not_type_list")
    category_type_list: List[Dict] = Field(..., description="category类型列表", title="category_type_list")


class CreateUserSchema(BaseModel):
    """创建用户Schema"""
    username: str = Field(..., description="用户名", title="username")
    password: str = Field(..., description="密码", title="password")
    email: str = Field(..., description="邮箱", title="email")
    phone: str = Field(..., description="手机号", title="phone")
    role_id: int = Field(..., description="角色id", title="role_id")
