from dataclasses import dataclass, field
from json import JSONDecodeError
from typing import Dict

import httpx

from pydockerhub.raw_http.errors import RawHttpConfigError
from pydockerhub.raw_http.types import RawHttpRequest, RawHttpResponse, RawHttpClient, HttpHeaders


@dataclass
class HttpxRequest:
    method: str
    url: str
    headers: Dict = field(default_factory=dict)
    params: Dict = field(default_factory=dict)
    json: Dict = field(default_factory=dict)
    follow_redirects: bool = True


@dataclass
class HttpxResponse:
    status_code: int
    successful: bool
    headers: HttpHeaders = field(default_factory=dict)
    body: Dict = field(default_factory=dict)


class HttpxClient(RawHttpClient):
    def make_request(self, request: RawHttpRequest) -> RawHttpResponse:
        if not hasattr(httpx, request.method.lower()):
            raise RawHttpConfigError(f'Invalid HTTP method: {request.method}')

        httpx_request = HttpxRequest(
            method=request.method.lower(),
            url=request.url,
            headers=request.headers,
            params=request.query_params,
            json=request.body
        )

        httpx_response = httpx.request(**httpx_request.__dict__)
        response_json = None

        try:
            response_json = httpx_response.json()
        except JSONDecodeError:
            pass

        return HttpxResponse(
            status_code=httpx_response.status_code,
            successful=httpx_response.is_success,
            headers=httpx_response.headers,
            body=response_json,
        )
