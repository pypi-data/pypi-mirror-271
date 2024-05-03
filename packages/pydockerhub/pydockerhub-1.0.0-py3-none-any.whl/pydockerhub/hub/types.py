from abc import ABC, abstractmethod
from typing import Dict

from pydockerhub.http_calls.response import HttpCallResponse


class ApiCaller(ABC):
    @abstractmethod
    def authorize(self, headers: Dict[str, str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def call(self, method_with_path: str, body: Dict = None, p: Dict = None, h: Dict = None) -> HttpCallResponse:
        raise NotImplementedError
