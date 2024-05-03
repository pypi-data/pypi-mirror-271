from typing import List

from exception import handle_exception
from pydockerhub.http_calls.caller import HttpClient
from pydockerhub.hub.models import Repository, Tag, SearchQuery, Credentials, Session, NewRepository
from pydockerhub.hub.types import ApiCaller


class PyDockerHub:
    def __init__(self, api_caller: ApiCaller):
        self.caller = api_caller
        self.credentials: Credentials | None = None

    @classmethod
    def with_caller(cls):
        return cls(api_caller=HttpClient())

    @classmethod
    def build_search(cls, page: int = 1, page_size: int = 100, ordering: str = '-name') -> SearchQuery:
        return SearchQuery(page=page, page_size=page_size, ordering=ordering)

    @handle_exception
    def login(self, credentials: Credentials) -> Session:
        response = self.caller.call('POST /users/login', body=credentials.model_dump())
        session = Session(**response.json_data)

        self.caller.authorize(session.as_header())
        self.credentials = credentials

        return session

    @handle_exception
    def search_repositories(self, query: SearchQuery) -> List[Repository]:
        response = self.caller.call(f'GET /repositories/{self.credentials.username}', p=query.model_dump())
        return [Repository(**repo) for repo in response.get_json_value(key='results')]

    @handle_exception
    def get_repository(self, name: str) -> Repository:
        response = self.caller.call(f'GET /repositories/{self.credentials.username}/{name}')
        return Repository(**response.json_data)

    @handle_exception
    def create_repository(self, name: str) -> None:
        payload = NewRepository(**{'namespace': self.credentials.username, 'name': name})
        self.caller.call('POST /repositories/', body=payload.model_dump())

    @handle_exception
    def delete_repository(self, name: str) -> None:
        self.caller.call(f'DELETE /repositories/{self.credentials.username}/{name}/')

    @handle_exception
    def search_repository_tags(self, name: str, query: SearchQuery) -> List[Tag]:
        response = self.caller.call(f'GET /repositories/{self.credentials.username}/{name}/tags', p=query.model_dump())
        return [Tag(**tag) for tag in response.get_json_value(key='results')]
