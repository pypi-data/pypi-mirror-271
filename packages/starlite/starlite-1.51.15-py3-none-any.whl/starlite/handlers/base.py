from copy import copy
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
    cast,
)

from pydantic import validate_arguments

from starlite.datastructures.provide import Provide
from starlite.exceptions import ImproperlyConfiguredException
from starlite.signature.models import SignatureField
from starlite.types import (
    Dependencies,
    Empty,
    EmptyType,
    ExceptionHandlersMap,
    Guard,
    Middleware,
    ParametersMap,
)
from starlite.utils import AsyncCallable, Ref, get_name, normalize_path
from starlite.utils.helpers import unwrap_partial

if TYPE_CHECKING:
    from inspect import Signature

    from starlite.connection import ASGIConnection
    from starlite.controller import Controller
    from starlite.router import Router
    from starlite.signature import SignatureModel
    from starlite.types import AnyCallable
    from starlite.types.composite_types import MaybePartial


T = TypeVar("T", bound="BaseRouteHandler")


class BaseRouteHandler(Generic[T]):
    """Base route handler.

    Serves as a subclass for all route handlers
    """

    fn: "Ref[MaybePartial[AnyCallable]]"
    signature: "Signature"

    __slots__ = (
        "_resolved_dependencies",
        "_resolved_guards",
        "_resolved_layered_parameters",
        "dependencies",
        "exception_handlers",
        "fn",
        "guards",
        "middleware",
        "name",
        "opt",
        "owner",
        "paths",
        "signature",
        "signature_model",
    )

    @validate_arguments(config={"arbitrary_types_allowed": True})
    def __init__(
        self,
        path: Union[Optional[str], Optional[List[str]]] = None,
        *,
        dependencies: Optional[Dependencies] = None,
        exception_handlers: Optional[ExceptionHandlersMap] = None,
        guards: Optional[List[Guard]] = None,
        middleware: Optional[List[Middleware]] = None,
        name: Optional[str] = None,
        opt: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize ``HTTPRouteHandler``.

        Args:
            path: A path fragment for the route handler function or a list of path fragments. If not given defaults to '/'
            dependencies: A string keyed dictionary of dependency :class:`Provider <starlite.datastructures.Provide>` instances.
            exception_handlers: A dictionary that maps handler functions to status codes and/or exception types.
            guards: A list of :class:`Guard <starlite.types.Guard>` callables.
            middleware: A list of :class:`Middleware <starlite.types.Middleware>`.
            name: A string identifying the route handler.
            opt: A string keyed dictionary of arbitrary values that can be accessed in :class:`Guards <starlite.types.Guard>` or
                wherever you have access to :class:`Request <starlite.connection.request.Request>` or :class:`ASGI Scope <starlite.types.Scope>`.
            **kwargs: Any additional kwarg - will be set in the opt dictionary.
        """
        self._resolved_dependencies: Union[Dict[str, "Provide"], "EmptyType"] = Empty
        self._resolved_guards: Union[List[Guard], EmptyType] = Empty
        self._resolved_layered_parameters: Union[Dict[str, "SignatureField"], "EmptyType"] = Empty
        self.dependencies = dependencies
        self.exception_handlers = exception_handlers
        self.guards = guards
        self.middleware = middleware
        self.name = name
        self.opt: Dict[str, Any] = opt or {}
        self.owner: Optional[Union["Controller", "Router"]] = None
        self.signature_model: Optional[Type["SignatureModel"]] = None
        self.paths = (
            {normalize_path(p) for p in path}
            if path and isinstance(path, list)
            else {normalize_path(path or "/")}  # type: ignore
        )
        self.opt.update(**kwargs)

    @property
    def handler_name(self) -> str:
        """Get the name of the handler function.

        Raises:
            ImproperlyConfiguredException: if handler fn is not set.

        Returns:
            Name of the handler function
        """
        fn = getattr(self, "fn", None)
        if not fn:
            raise ImproperlyConfiguredException("cannot access handler name before setting the handler function")
        return get_name(unwrap_partial(self.fn.value))

    @property
    def dependency_name_set(self) -> Set[str]:
        """Set of all dependency names provided in the handler's ownership layers."""
        layered_dependencies = (layer.dependencies or {} for layer in self.ownership_layers)
        return {name for layer in layered_dependencies for name in layer.keys()}

    @property
    def ownership_layers(self) -> List[Union[T, "Controller", "Router"]]:
        """Return the handler layers from the app down to the route handler.

        app -> ... -> route handler
        """
        layers = []

        cur: Any = self
        while cur:
            layers.append(cur)
            cur = cur.owner

        return list(reversed(layers))

    def resolve_layered_parameters(self) -> Dict[str, "SignatureField"]:
        """Return all parameters declared above the handler."""
        if self._resolved_layered_parameters is Empty:
            parameter_kwargs: "ParametersMap" = {}

            for layer in self.ownership_layers:
                parameter_kwargs.update(getattr(layer, "parameters", {}) or {})

            self._resolved_layered_parameters = {
                key: SignatureField.create(
                    name=key, field_type=parameter.value_type, default_value=parameter.default, kwarg_model=parameter
                )
                for key, parameter in parameter_kwargs.items()
            }

        return cast("Dict[str, SignatureField]", self._resolved_layered_parameters)

    def resolve_guards(self) -> List[Guard]:
        """Return all guards in the handlers scope, starting from highest to current layer."""
        if self._resolved_guards is Empty:
            self._resolved_guards = []

            for layer in self.ownership_layers:
                self._resolved_guards.extend(layer.guards or [])

            self._resolved_guards = cast("List[Guard]", [AsyncCallable(guard) for guard in self._resolved_guards])

        return self._resolved_guards  # type:ignore

    def resolve_dependencies(self) -> Dict[str, Provide]:
        """Return all dependencies correlating to handler function's kwargs that exist in the handler's scope."""
        if self._resolved_dependencies is Empty:
            self._resolved_dependencies = {}

            for layer in self.ownership_layers:
                for key, value in (layer.dependencies or {}).items():
                    self._validate_dependency_is_unique(
                        dependencies=self._resolved_dependencies, key=key, provider=value
                    )
                    self._resolved_dependencies[key] = value

        return cast("Dict[str, Provide]", self._resolved_dependencies)

    def resolve_middleware(self) -> List["Middleware"]:
        """Build the middleware stack for the RouteHandler and return it.

        The middlewares are added from top to bottom (app -> router -> controller -> route handler) and then reversed.
        """
        resolved_middleware = []
        for layer in self.ownership_layers:
            resolved_middleware.extend(layer.middleware or [])
        return list(reversed(resolved_middleware))

    def resolve_exception_handlers(self) -> ExceptionHandlersMap:
        """Resolve the exception_handlers by starting from the route handler and moving up.

        This method is memoized so the computation occurs only once.
        """
        resolved_exception_handlers = {}
        for layer in self.ownership_layers:
            resolved_exception_handlers.update(layer.exception_handlers or {})
        return resolved_exception_handlers

    def resolve_opts(self) -> None:
        """Build the route handler opt dictionary by going from top to bottom.

        If multiple layers define the same key, the value from the closest layer to the response handler will take
        precedence.
        """

        opt: Dict[str, Any] = {}
        for layer in self.ownership_layers:
            opt.update(layer.opt or {})

        self.opt = opt

    async def authorize_connection(self, connection: "ASGIConnection") -> None:
        """Ensure the connection is authorized by running all the route guards in scope."""
        for guard in self.resolve_guards():
            await guard(connection, copy(self))  # type: ignore

    @staticmethod
    def _validate_dependency_is_unique(dependencies: Dict[str, Provide], key: str, provider: Provide) -> None:
        """Validate that a given provider has not been already defined under a different key."""
        for dependency_key, value in dependencies.items():
            if provider == value:
                raise ImproperlyConfiguredException(
                    f"Provider for key {key} is already defined under the different key {dependency_key}. "
                    f"If you wish to override a provider, it must have the same key."
                )

    def _validate_handler_function(self) -> None:
        """Validate the route handler function once set by inspecting its return annotations."""
        if not getattr(self, "fn", None):
            raise ImproperlyConfiguredException("Cannot call _validate_handler_function without first setting self.fn")

    def __str__(self) -> str:
        """Return a unique identifier for the route handler.

        Returns:
            A string
        """
        target = unwrap_partial(self.fn.value)
        if not hasattr(target, "__qualname__"):
            target = type(target)
        return f"{target.__module__}.{target.__qualname__}"
