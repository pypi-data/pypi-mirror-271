from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class Credentials(BaseModel):
    username: str
    password: str


class Session(BaseModel):
    token: str

    def as_header(self) -> Dict[str, str]:
        return {'Authorization': f'JWT {self.token}'}


class Registry(BaseModel):
    namespace: str


class Repository(BaseModel):
    namespace: str
    name: str


class NewRepository(BaseModel):
    namespace: str
    name: str
    description: str = ''
    registry: str = 'docker'
    is_private: bool = False


class Tag(BaseModel):
    name: str
    created_at: datetime = Field(..., alias='last_updated')


class PathParams(BaseModel):
    namespace: str = ''
    repository: str = ''


class SearchQuery(BaseModel):
    page: int = 1
    page_size: int = 100
    ordering: str = 'name'
