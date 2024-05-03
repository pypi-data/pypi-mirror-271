from pydockerhub.api_calls.errors import ApiCallError
from pydockerhub.api_calls.request import RequestConfig, ApiCallRequest
from pydockerhub.api_calls.response import ApiCallResponse
from pydockerhub.hub.models import PathParams, Session
from pydockerhub.hub.types import ApiCaller, ApiCall
from pydockerhub.raw_http.client import HttpxClient
from pydockerhub.raw_http.types import RawHttpClient


class HttpCaller(ApiCaller):
    def __init__(self, config: RequestConfig | None = None):
        self._config = config if config is not None else RequestConfig()
        self._http_client: RawHttpClient = HttpxClient()

    def authenticate_calls(self, session: Session) -> None:
        self._config = self._config.with_headers(session.as_header())

    def call(self, api_call: ApiCall, path_params: PathParams | None = None) -> ApiCallResponse:
        resolved_path = api_call.resolve_path(path_params) if path_params else api_call.get_path()
        method, path = resolved_path.split(' ')

        request = ApiCallRequest(
            method=method,
            url=self._config.make_url(path),
            headers=self._config.headers,
            query_params=api_call.get_query_params(),
            body=api_call.get_body(),
        )

        response = self._http_client.make_request(request=request)

        if not response.successful:
            raise ApiCallError(f'Call to API failed with message: {response.body}')

        return ApiCallResponse(
            status_code=response.status_code,
            successful=response.successful,
            headers=response.headers,
            body=response.body,
        )
