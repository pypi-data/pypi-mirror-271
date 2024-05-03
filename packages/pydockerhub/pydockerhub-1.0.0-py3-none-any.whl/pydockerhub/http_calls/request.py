from typing import Dict

from pydantic import BaseModel


class RequestConfig(BaseModel):
    base_url: str = 'https://hub.docker.com/v2'
    headers: Dict[str, str] = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
        'Origin': 'https://hub.docker.com',
    }

    def with_headers(self, headers: Dict[str, str]) -> 'RequestConfig':
        merged_headers = self.headers | headers
        return RequestConfig(headers=merged_headers)

    @staticmethod
    def with_replaced_headers(headers: Dict[str, str]) -> 'RequestConfig':
        return RequestConfig(headers=headers)
