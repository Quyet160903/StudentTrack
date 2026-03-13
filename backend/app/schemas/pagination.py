import math
from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
from fastapi import Query

T = TypeVar("T")


class PaginationParams:
    """
    Reusable dependency — inject into any route that needs pagination.

    FastAPI will automatically read ?page=1&page_size=10 from the URL.
    """
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number, starts at 1"),
        page_size: int = Query(default=10, ge=1, le=100, description="Items per page, max 100"),
    ):
        self.page = page
        self.page_size = page_size

        # Calculate SQL OFFSET from page number
        # page=1 → offset=0, page=2 → offset=10, page=3 → offset=20 ...
        self.offset = (page - 1) * page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response wrapper.

    Generic[T] means this schema works for ANY type:
        PaginatedResponse[JobResponse]
        PaginatedResponse[StudentResponse]
        PaginatedResponse[ApplicationResponse]
    """
    items: List[T]                          # the actual data for this page
    total: int                              # total records in DB matching the query
    page: int                               # current page number
    page_size: int                          # items per page
    total_pages: int                        # calculated automatically

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams):
        """
        Helper factory method so you don't have to calculate total_pages manually.

        Usage:
            return PaginatedResponse.create(items=jobs, total=total, params=params)
        """
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=math.ceil(total / params.page_size) if params.page_size > 0 else 0,
        )