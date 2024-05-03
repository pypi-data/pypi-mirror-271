import json
from typing import Dict, Tuple
import logging
import httpx
from pydockerhub.http_calls.request import RequestConfig
from pydockerhub.http_calls.response import HttpCallResponse
from pydockerhub.http_calls.errors import HttpCallError
from pydockerhub.hub.types import ApiCaller

logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)


class HttpClient(ApiCaller):
    def __init__(self, config: RequestConfig | None = None):
        self._config = config if config is not None else RequestConfig()

    def authorize(self, headers: Dict[str, str]) -> None:
        self._config = self._config.with_headers(headers)

    def _unpack_request(self, method_with_path: str, _headers: Dict | None = None) -> Tuple[str, str, Dict]:
        method, path = method_with_path.split(' ')
        if not hasattr(httpx, method.lower()):
            raise HttpCallError(f'Invalid HTTP method: {method}')

        headers = self._config.headers | _headers if _headers is not None else self._config.headers
        return method, f'{self._config.base_url}{path}', headers

    def call(self, method_with_path: str, body: Dict = None, p: Dict = None, h: Dict = None) -> HttpCallResponse:
        method, url, headers = self._unpack_request(method_with_path, h)
        response = httpx.request(method, url, json=body, params=p, headers=headers, follow_redirects=True)

        try:
            response_json = response.json()
        except json.JSONDecodeError:
            response_json = {}

        if response.is_error:
            message = response_json['message'] if 'message' in response_json else 'JSON-less response'
            raise HttpCallError(message)

        return HttpCallResponse(status_code=response.status_code, json_data=response_json)
