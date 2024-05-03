from dataclasses import dataclass
from typing import Dict

from pydockerhub.hub.models import SearchQuery, NewRepository, Credentials
from pydockerhub.hub.types import ApiCall


@dataclass
class CreateSession(ApiCall):
    body: Credentials

    def get_path(self) -> str:
        return 'POST /users/login'

    def get_body(self) -> Dict:
        return self.body.model_dump()


@dataclass
class SearchRepositories(ApiCall):
    search: SearchQuery

    def get_path(self) -> str:
        return 'GET /repositories/{namespace}/'

    def get_query_params(self) -> Dict[str, str]:
        return self.search.model_dump()


@dataclass
class GetRepository(ApiCall):
    def get_path(self) -> str:
        return 'GET /repositories/{namespace}/{repository}'


@dataclass
class CreateRepository(ApiCall):
    body: NewRepository

    def get_path(self) -> str:
        return 'POST /repositories/'

    def get_body(self) -> Dict:
        return self.body.model_dump()


@dataclass
class DeleteRepository(ApiCall):
    def get_path(self) -> str:
        return 'DELETE /repositories/{namespace}/{repository}'


@dataclass
class SearchRepositoryTags(ApiCall):
    search: SearchQuery

    def get_path(self) -> str:
        return 'GET /repositories/{namespace}/{repository}/tags'

    def get_query_params(self) -> Dict[str, str]:
        return self.search.model_dump()
