from dataclasses import dataclass, field
from typing import Dict

from pydantic import BaseModel


@dataclass
class ApiCallRequest:
    url: str
    method: str
    headers: Dict[str, str] = field(default_factory=dict)
    query_params: Dict[str, str] = field(default_factory=dict)
    body: Dict = field(default_factory=dict)


class RequestConfig(BaseModel):
    base_url: str = 'https://hub.docker.com/v2'
    headers: Dict[str, str] = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
        'Origin': 'https://hub.docker.com',
    }

    @staticmethod
    def with_replaced_base_url(base_url: str) -> 'RequestConfig':
        return RequestConfig(base_url=base_url)

    @staticmethod
    def with_replaced_headers(headers: Dict[str, str]) -> 'RequestConfig':
        return RequestConfig(headers=headers)

    def make_url(self, path: str) -> str:
        return f'{self.base_url}{path}'

    def with_headers(self, headers: Dict[str, str]) -> 'RequestConfig':
        merged_headers = self.headers | headers
        return RequestConfig(headers=merged_headers)
