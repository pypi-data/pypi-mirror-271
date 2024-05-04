from pydantic import BaseModel
from typing import Optional


class Page(BaseModel):
    """
    Attributes:
        pageNum: 页码.
        pageSize: 每页数量.
    """
    pageNum: int = 1
    pageSize: Optional[int] = 100
    totalCount: Optional[int] = 1
    totalPage: Optional[int] = 1
