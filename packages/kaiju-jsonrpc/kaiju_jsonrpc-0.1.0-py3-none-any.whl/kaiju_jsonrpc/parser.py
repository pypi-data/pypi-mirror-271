"""Request parser types."""
from collections.abc import Mapping
from time import time
from typing import (Any, Awaitable, Callable, Collection, NamedTuple,
                    TypeAlias, TypedDict, cast, final)

from kaiju_app import Error as BaseError

from kaiju_jsonrpc.router import Router

__all__ = ['HTTPHeader', 'JSONHeader', 'RequestHeaders', 'MethodNotFound', 'InvalidRequest', 'InvalidParams', 'Parser',
           'Request', 'RequestId', 'Response', 'Error', 'ErrorData', 'BatchRequest', 'BatchResponse', 'RPCError']

_Func: TypeAlias = Callable[..., Awaitable[Any]]


@final
class HTTPHeader:
    """Set of standard RPC headers."""

    rpc_timeout = b"timeout"
    rpc_deadline = b"deadline"
    rpc_batch_abort_on_error = b"rpc-batch-abort-on-error"
    rpc_retries = b"rpc-retries"


@final
class JSONHeader:
    """Set of standard RPC headers."""

    rpc_timeout = "timeout"
    rpc_deadline = "deadline"
    rpc_retries = "rpc-retries"
    rpc_batch_abort_on_error = "rpc-batch-abort-on-error"


class RequestHeaders(NamedTuple):
    timeout_s: float
    deadline: int | None
    retries: int
    batch_abort_on_error: bool


RequestId: TypeAlias = int | str | bytes | None


class Request(TypedDict):
    id: RequestId
    method: str
    params: dict | None


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
BatchResponse: TypeAlias = Collection[Response]


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
            headers: Mapping[str, Any], *,
            default_request_timeout_s: float, max_request_timeout_s: float, max_request_retries: int,
    ) -> RequestHeaders:
        """Parse request headers with JSON compatible data types."""
        if JSONHeader.rpc_timeout in headers:
            timeout = max(0., min(max_request_timeout_s, headers[JSONHeader.rpc_timeout]))
        else:
            timeout = default_request_timeout_s
        deadline = headers.get(JSONHeader.rpc_deadline)
        if deadline:
            timeout = min(deadline - time(), timeout)
        if JSONHeader.rpc_retries in headers:
            retries = max(0, min(max_request_retries, headers[JSONHeader.rpc_retries]))
        else:
            retries = 0
        abort_on_error = headers.get(JSONHeader.rpc_batch_abort_on_error, True)
        return RequestHeaders(timeout, deadline, retries, abort_on_error)

    @staticmethod
    def get_request_headers_http(
            headers: Mapping[bytes, bytes], *,
            default_request_timeout_s: float, max_request_timeout_s: float, max_request_retries: int,
    ) -> RequestHeaders:
        """Parse request headers with HTTP binary strings."""
        if HTTPHeader.rpc_timeout in headers:
            timeout = max(0., min(max_request_timeout_s, float(headers[HTTPHeader.rpc_timeout])))
        else:
            timeout = default_request_timeout_s
        if HTTPHeader.rpc_deadline in headers:
            deadline = int(headers[HTTPHeader.rpc_deadline])
            timeout = min(deadline - time(), timeout)
        else:
            deadline = None
        if HTTPHeader.rpc_retries in headers:
            retries = max(0, min(max_request_retries, int(headers[HTTPHeader.rpc_retries])))
        else:
            retries = 0
        if HTTPHeader.rpc_batch_abort_on_error in headers:
            abort_on_error = bool(int(headers[HTTPHeader.rpc_batch_abort_on_error]))
        else:
            abort_on_error = True
        return RequestHeaders(timeout, deadline, retries, abort_on_error)

    @staticmethod
    def get_request_call_args(router: Router, method: str, params: Any, permission: int) -> tuple[_Func, dict]:
        """Get server call args."""
        method_data = router.get(method)
        if method_data is None or method_data.permission < permission:
            raise MethodNotFound(method) from None
        if params is None:
            params = {}
            if method_data.keys_required:
                raise InvalidParams(
                    f'Missing required input params.', missing_keys=list(method_data.keys_required)
                ) from None
        elif not isinstance(params, Mapping):
            raise InvalidRequest(
                'Method params must be either null or an object.'
            ) from None
        else:
            if not method_data.keys_required.issubset(params) or not method_data.keys.issuperset(params):
                raise InvalidParams(
                    'Invalid request params.',
                    required_keys=method_data.keys_required,
                    allowed_keys=method_data.keys
                ) from None
        if method_data.validator:
            try:
                params = method_data.validator(params)
            except Exception as exc:
                raise InvalidParams(str(exc), method=method, params=params, schema=method_data.schema)
        return method_data.func, cast(dict, params)
