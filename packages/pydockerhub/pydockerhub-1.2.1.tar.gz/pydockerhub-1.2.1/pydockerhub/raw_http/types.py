from abc import ABC, abstractmethod
from typing import Protocol, Optional, Dict

from pydockerhub.api_calls.types import JsonData

HttpQueryParams = Dict[str, str]
HttpPathParams = Dict[str, str]
HttpHeaders = Dict[str, str]


class RawHttpRequest(Protocol):
    url: str
    method: str
    headers: HttpHeaders
    query_params: Optional[HttpQueryParams]
    body: Optional[str | JsonData]


class RawHttpResponse(Protocol):
    status_code: int
    successful: bool
    headers: HttpHeaders
    body: Optional[str | JsonData]


class RawHttpClient(ABC):
    @abstractmethod
    def make_request(self, request: RawHttpRequest) -> RawHttpResponse:
        raise NotImplementedError
