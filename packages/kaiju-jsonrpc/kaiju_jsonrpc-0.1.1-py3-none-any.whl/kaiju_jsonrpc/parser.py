"""Request parser types."""

from time import time
from typing import Any, Awaitable, Callable, Collection, NamedTuple, TypeAlias, TypedDict, cast, final, Mapping

from kaiju_app import Error as BaseError

from kaiju_jsonrpc.router import Router

__all__ = [
    "Header",
    "TypeId",
    "RequestHeaders",
    "MethodNotFound",
    "InvalidRequest",
    "InvalidParams",
    "Parser",
    "Request",
    "RequestId",
    "Response",
    "Error",
    "ErrorData",
    "BatchRequest",
    "BatchResponse",
    "AnyResponse",
    "RPCError",
]

_Func: TypeAlias = Callable[..., Awaitable[Any]]


@final
class Header:
    """Set of standard RPC headers."""

    correlation_id = 'correlation-id'
    rpc_timeout = "timeout"
    rpc_deadline = "deadline"
    rpc_batch_abort_on_error = "rpc-batch-abort-on-error"
    rpc_retries = "rpc-retries"


@final
class TypeId:
    request = 17
    response = 18
    error = 19


class RequestHeaders(NamedTuple):
    timeout_s: float
    deadline: int | None
    retries: int
    batch_abort_on_error: bool


RequestId: TypeAlias = int | None


class Request(TypedDict):
    id: RequestId
    method: str
    params: Mapping[str, Any] | None


class Response(TypedDict):
    id: RequestId
    result: Any


class ErrorData(TypedDict):
    code: int
    message: str
    data: dict[str, Any] | None


class Error(TypedDict):
    id: RequestId
    error: ErrorData


BatchRequest: TypeAlias = Collection[Request]
BatchResponse: TypeAlias = Collection[Response | Error]
AnyResponse: TypeAlias = BatchResponse | Response | Error
RequestTuple: TypeAlias = tuple[int, RequestId, str, Mapping[str, Any] | None]
ResponseTuple: TypeAlias = tuple[int, RequestId, Any]
ErrorTuple: TypeAlias = tuple[int, RequestId, int, str, dict[str, Any] | None]
BatchRequestTuple: TypeAlias = Collection[RequestTuple]
BatchResponseTuple: TypeAlias = Collection[ResponseTuple | ErrorTuple]
AnyRequestTuple: TypeAlias = RequestTuple | BatchRequestTuple
AnyResponseTuple: TypeAlias = ResponseTuple | ErrorTuple | BatchResponseTuple


class RPCError(BaseError):
    code = -32603


class MethodNotFound(RPCError):
    code = -32601


class InvalidRequest(RPCError):
    code = -32600


class InvalidParams(RPCError):
    code = -32602


class Parser:
    """RPC request header and body parser."""

    @staticmethod
    def get_request_headers_json(
        headers: Mapping[str, Any],
        *,
        default_request_timeout_s: float,
        max_request_timeout_s: float,
        max_request_retries: int,
    ) -> RequestHeaders:
        """Parse request headers with JSON compatible data types."""
        if Header.rpc_timeout in headers:
            timeout = max(0.0, min(max_request_timeout_s, headers[Header.rpc_timeout]))
        else:
            timeout = default_request_timeout_s
        deadline = headers.get(Header.rpc_deadline)
        if deadline:
            timeout = min(deadline - time(), timeout)
        if Header.rpc_retries in headers:
            retries = max(0, min(max_request_retries, headers[Header.rpc_retries]))
        else:
            retries = 0
        abort_on_error = headers.get(Header.rpc_batch_abort_on_error, True)
        return RequestHeaders(timeout, deadline, retries, abort_on_error)

    @staticmethod
    def get_request_headers_http(
        headers: Mapping[str, bytes | str],
        *,
        default_request_timeout_s: float,
        max_request_timeout_s: float,
        max_request_retries: int,
    ) -> RequestHeaders:
        """Parse request headers with HTTP binary strings."""
        if Header.rpc_timeout in headers:
            timeout = max(0.0, min(max_request_timeout_s, float(headers[Header.rpc_timeout])))
        else:
            timeout = default_request_timeout_s
        if Header.rpc_deadline in headers:
            deadline = int(headers[Header.rpc_deadline])
            timeout = min(deadline - time(), timeout)
        else:
            deadline = None
        if Header.rpc_retries in headers:
            retries = max(0, min(max_request_retries, int(headers[Header.rpc_retries])))
        else:
            retries = 0
        if Header.rpc_batch_abort_on_error in headers:
            abort_on_error = bool(int(headers[Header.rpc_batch_abort_on_error]))
        else:
            abort_on_error = True
        return RequestHeaders(timeout, deadline, retries, abort_on_error)

    @classmethod
    def get_request_params(cls, request_body: Mapping[str, Any], /) -> tuple[RequestId, str, dict[str, Any] | None]:
        request_id = request_body['id'] if 'id' in request_body else None
        if type(request_id) is not int:
            raise InvalidRequest('Request id must be integer')
        if 'method' not in request_body:
            raise InvalidRequest("Missing method parameter")
        method_name = request_body['method']
        if type(method_name) is not str:
            raise InvalidRequest("Method must be a string")
        params = request_body.get('params')
        if params is not None and not hasattr(params, '__getitem__'):
            raise InvalidRequest('Request params must be a mapping (dictionary object)')
        return request_id, method_name, params

    @staticmethod
    def get_server_call_args(router: Router, method: str, params: Mapping[str, Any] | None, permission: int) -> tuple[_Func, Mapping[str, Any]]:
        method_data = router.get(method)
        if method_data is None or method_data.permission < permission:
            raise MethodNotFound(method)
        kws = {k: v for k, v in params.items() if not k.startswith('_')} if params else {}
        if not method_data.keys_required.issubset(kws) or not method_data.keys.issuperset(kws):
            raise InvalidParams(
                "Invalid request params.", required_keys=method_data.keys_required, allowed_keys=method_data.keys
            )
        if method_data.validator:
            try:
                kws = method_data.validator(kws)
            except Exception as exc:
                raise InvalidParams(str(exc), method=method, params=params, schema=method_data.schema)
        return method_data.func, cast(dict, kws)
