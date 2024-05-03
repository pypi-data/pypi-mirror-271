from typing import List

from pydockerhub.api_calls.caller import HttpCaller
from pydockerhub.exception import handle_exception
from pydockerhub.hub import actions
from pydockerhub.hub.models import Repository, Tag, SearchQuery, Credentials, Session, NewRepository, PathParams
from pydockerhub.hub.types import ApiCaller


class PyDockerHub:
    def __init__(self, api_caller: ApiCaller):
        self.caller = api_caller
        self.credentials: Credentials | None = None

    def _build_path_params(self, repository: str = '') -> PathParams:
        return PathParams(namespace=self.credentials.username, repository=repository)

    @classmethod
    def with_caller(cls):
        return cls(api_caller=HttpCaller())

    @classmethod
    def build_search(cls, page: int = 1, page_size: int = 100, ordering: str = '-name') -> SearchQuery:
        return SearchQuery(page=page, page_size=page_size, ordering=ordering)

    @handle_exception
    def login(self, credentials: Credentials) -> Session:
        response = self.caller.call(actions.CreateSession(body=credentials))
        session = Session(**response.body)

        self.caller.authenticate_calls(session)
        self.credentials = credentials

        return session

    @handle_exception
    def search_repositories(self, search: SearchQuery) -> List[Repository]:
        response = self.caller.call(actions.SearchRepositories(search=search), self._build_path_params())
        return [Repository(**repo) for repo in response.get_json_value(key='results')]

    @handle_exception
    def get_repository(self, repository: str) -> Repository:
        response = self.caller.call(actions.GetRepository(), self._build_path_params(repository))
        return Repository(**response.body)

    @handle_exception
    def create_repository(self, repository: str) -> None:
        data = self._build_path_params(repository).model_dump()
        data['name'] = data.pop('repository')
        self.caller.call(actions.CreateRepository(body=NewRepository(**data)))

    @handle_exception
    def delete_repository(self, repository: str) -> None:
        self.caller.call(actions.DeleteRepository(), self._build_path_params(repository))

    @handle_exception
    def search_repository_tags(self, repository: str, search: SearchQuery) -> List[Tag]:
        response = self.caller.call(actions.SearchRepositoryTags(search=search), self._build_path_params(repository))
        return [Tag(**tag) for tag in response.get_json_value(key='results')]
