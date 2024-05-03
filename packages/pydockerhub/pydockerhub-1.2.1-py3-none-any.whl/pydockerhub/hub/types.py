from abc import ABC, abstractmethod
from typing import Dict

from pydockerhub.api_calls.response import ApiCallResponse
from pydockerhub.hub.models import Session, PathParams


class ApiCall(ABC):
    @abstractmethod
    def get_path(self) -> str:
        raise NotImplementedError

    def get_query_params(self) -> Dict[str, str]:
        ...

    def get_body(self) -> Dict:
        ...

    def resolve_path(self, params: PathParams) -> str:
        return self.get_path().format(**params.model_dump())


class ApiCaller(ABC):
    @abstractmethod
    def authenticate_calls(self, session: Session) -> None:
        raise NotImplementedError

    @abstractmethod
    def call(self, api_call: ApiCall, path_params: PathParams | None = None) -> ApiCallResponse:
        raise NotImplementedError
