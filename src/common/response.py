from typing import TypeVar, Generic, Optional

from pydantic.v1.generics import GenericModel

T = TypeVar("T")


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    result: Optional[T]
