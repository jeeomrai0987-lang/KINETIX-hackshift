from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

T = TypeVar("T")

class ListResponse(CamelModel, Generic[T]):
    items: List[T]
    total: int

class ErrorDetail(CamelModel):
    code: str
    message: str

class ErrorResponse(CamelModel):
    error: ErrorDetail
