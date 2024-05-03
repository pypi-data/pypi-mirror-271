"""RPC router."""
import inspect
from abc import abstractmethod
from collections.abc import Collection
from dataclasses import dataclass, field
from fnmatch import fnmatch
from typing import (Any, Awaitable, Callable, ClassVar, Mapping, NamedTuple,
                    Protocol, TypeAlias, TypeGuard, cast, final)

from fastjsonschema import compile as compile_schema
from jsonschema_gen import Parser as AnnotationParser
from jsonschema_gen.schema import JSONSchemaObject, JSONSchemaType
from kaiju_app import Application

__all__ = ["Router", 'Method', "RPCInterface", "is_rpc_interface"]


ValidatorType: TypeAlias = Callable[[Mapping[str, Any]], Mapping[str, Any]] | JSONSchemaType


@final
class Method(NamedTuple):
    func: Callable[..., Awaitable]
    permission: int = 0
    validator: ValidatorType | None = None


class RPCInterface(Protocol):

    name: str | None

    @classmethod
    @abstractmethod
    def rpc_routes(cls) -> dict[str, Method | Callable[..., Awaitable]]: ...


def is_rpc_interface(obj, /) -> TypeGuard[RPCInterface]:
    return hasattr(obj, "rpc_routes")


@final
class _Method(NamedTuple):
    func: Callable[..., Awaitable]
    keys: frozenset[str]
    keys_required: frozenset[str]
    permission: int
    schema: JSONSchemaType
    validator: ValidatorType | None


@dataclass
class Router(Mapping[str, _Method]):
    """Router for RPC methods.

    It contains a map of RPC routes to Python methods, validators, permissions, etc.
    """

    private_key_prefix: ClassVar[str] = '_'
    """Ignore method input parameters starting with such prefix."""

    auto_create_validators: bool = True
    """Auto-create validators for methods with missing validators."""

    whitelist_routes: Collection[str] = field(default=tuple())
    """Whitelist of routes or route patterns, by default it's all of them."""

    _routes: dict[str, _Method] = field(default_factory=dict)
    _parser: AnnotationParser = field(default_factory=AnnotationParser)

    def __getitem__(self, route: str, /) -> _Method:
        return self._routes[route]

    def __len__(self):
        return len(self._routes)

    def __iter__(self):
        return iter(self._routes)

    def clear(self):
        self._routes.clear()

    def json_repr(self) -> dict[str, Any]:
        routes = [
            {"id": route, "permission": method.permission, "schema": method.schema}
            for route, method in self._routes.items()
        ]
        routes.sort(key=lambda route: route["id"])
        return {"routes": routes}

    def add_routes_from_app(self, app: Application, /) -> None:
        for name, service in app.services.items():
            if is_rpc_interface(service):
                self.add_routes_from_interface(cast(RPCInterface, service), name=name)

    def add_routes_from_interface(self, interface: RPCInterface, /, name: str | None = None) -> None:
        if name is None:
            name = getattr(interface, "name", interface.__class__.__name__)
        for route, method in interface.rpc_routes().items():
            full_route = f"{name}.{route}"
            if not self.is_in_whitelist(full_route):
                continue
            if not isinstance(method, Method):
                method = Method(func=method)
            schema, validator = self._create_method_validator(interface, method)
            keys, keys_required = self._get_method_kws(method.func)
            self._routes[full_route] = _Method(
                func=method.func, permission=method.permission, schema=schema, validator=validator,
                keys=keys, keys_required=keys_required
            )

    def is_in_whitelist(self, route: str, /) -> bool:
        """Check if a route is allowed."""
        if not self.whitelist_routes:
            return True
        for pattern in self.whitelist_routes:
            if route == pattern or fnmatch(route, pattern):
                return True
        return False

    def _get_method_kws(self, func: Callable[..., Awaitable]) -> tuple[frozenset[str], frozenset[str]]:
        sig = inspect.signature(func)
        keys, keys_required = [], []
        for key in sig.parameters.values():
            if key.kind == key.VAR_KEYWORD:
                continue
            elif key.kind == key.VAR_POSITIONAL:
                continue
            elif key.name.startswith(self.private_key_prefix):
                continue
            keys.append(key.name)
            if key.default is key.empty:
                keys_required.append(key.name)
        return frozenset(keys), frozenset(keys_required)

    def _create_method_validator(
        self, interface: RPCInterface, method: Method, /
    ) -> tuple[JSONSchemaType, ValidatorType]:
        validator = method.validator
        try:
            schema = self._parser.parse_function(method.func, type(interface))
        except Exception:
            schema = JSONSchemaObject(title="!unsupported type")
        else:
            if self.auto_create_validators and method.validator is None:
                validator = schema
        if validator is not None and hasattr(validator, "json_repr"):
            validator = compile_schema(validator.json_repr())
        return schema, validator
