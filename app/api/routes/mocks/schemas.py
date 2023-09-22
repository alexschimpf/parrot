import enum
from typing import Any
from pydantic import BaseModel, Field


class HTTPMethod(enum.StrEnum):
    GET = 'GET'
    PATCH = 'POST'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'


class Mock(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    method: HTTPMethod
    path: str = Field(min_length=1)
    query_params: dict[str, str] | None = None
    headers: dict[str, str] | None = None
    cookies: dict[str, str] | None = None
    response_body: dict[Any, Any] | None = None
    response_handler: str | None = None
    response_status: int | None = None
    response_headers: dict[str, str] | None = None


class Mocks(BaseModel):
    mocks: list[Mock]


class MockNames(BaseModel):
    names: list[str]
