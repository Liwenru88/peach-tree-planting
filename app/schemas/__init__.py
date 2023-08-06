from typing import Union, List, Dict, Optional

from pydantic import BaseModel

from app.utils.define import StatusCode


class ResponseSchema(BaseModel):
    """ResponseSchema"""
    code: int = StatusCode.success
    message: str = None
    data: Union[List, Dict] = None
    currentPage: Optional[int]
    totalCount: Optional[int]
