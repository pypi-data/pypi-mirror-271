import re
from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union
from uuid import UUID

from pydantic.datetime_parse import (
    parse_date,
    parse_datetime,
    parse_duration,
    parse_time,
)

from starlite.exceptions import ImproperlyConfiguredException
from starlite.kwargs import KwargsModel
from starlite.signature import get_signature_model
from starlite.types.internal_types import PathParameterDefinition
from starlite.utils import join_paths, normalize_path

if TYPE_CHECKING:
    from starlite.enums import ScopeType
    from starlite.handlers.base import BaseRouteHandler
    from starlite.types import Method, Receive, Scope, Send

param_match_regex = re.compile(r"{(.*?)}")

param_type_map = {
    "str": str,
    "int": int,
    "float": float,
    "uuid": UUID,
    "decimal": Decimal,
    "date": date,
    "datetime": datetime,
    "time": time,
    "timedelta": timedelta,
    "path": Path,
}


parsers_map: Dict[Any, Callable[[Any], Any]] = {
    float: float,
    int: int,
    Decimal: Decimal,
    UUID: UUID,
    date: parse_date,
    datetime: parse_datetime,
    time: parse_time,
    timedelta: parse_duration,
}


class BaseRoute(ABC):
    """Base Route class used by Starlite.

    It's an abstract class meant to be extended.
    """

    __slots__ = (
        "app",
        "handler_names",
        "methods",
        "path",
        "path_format",
        "path_parameters",
        "path_components",
        "scope_type",
    )

    def __init__(
        self,
        *,
        handler_names: List[str],
        path: str,
        scope_type: "ScopeType",
        methods: Optional[List["Method"]] = None,
    ) -> None:
        """Initialize the route.

        Args:
            handler_names: Names of the associated handler functions
            path: Base path of the route
            scope_type: Type of the ASGI scope
            methods: Supported methods
        """
        self.path, self.path_format, self.path_components = self._parse_path(path)
        self.path_parameters: Tuple[PathParameterDefinition, ...] = tuple(
            component for component in self.path_components if isinstance(component, PathParameterDefinition)
        )
        self.handler_names = handler_names
        self.scope_type = scope_type
        self.methods = set(methods or [])

    @abstractmethod
    async def handle(self, scope: "Scope", receive: "Receive", send: "Send") -> None:  # pragma: no cover
        """ASGI App of the route.

        Args:
            scope: The ASGI connection scope.
            receive: The ASGI receive function.
            send: The ASGI send function.

        Returns:
            None
        """
        raise NotImplementedError("Route subclasses must implement handle which serves as the ASGI app entry point")

    def create_handler_kwargs_model(self, route_handler: "BaseRouteHandler") -> KwargsModel:
        """Create a `KwargsModel` for a given route handler."""

        path_parameters = set()
        for param in self.path_parameters:
            if param.name in path_parameters:
                raise ImproperlyConfiguredException(f"Duplicate parameter '{param.name}' detected in '{self.path}'.")
            path_parameters.add(param.name)

        return KwargsModel.create_for_signature_model(
            signature_model=get_signature_model(route_handler),
            dependencies=route_handler.resolve_dependencies(),
            path_parameters=path_parameters,
            layered_parameters=route_handler.resolve_layered_parameters(),
        )

    @staticmethod
    def _validate_path_parameter(param: str) -> None:
        """Validate that a path parameter adheres to the required format and datatypes.

        Raises:
            ImproperlyConfiguredException: If the parameter has an invalid format.
        """
        if len(param.split(":")) != 2:
            raise ImproperlyConfiguredException(
                "Path parameters should be declared with a type using the following pattern: '{parameter_name:type}', e.g. '/my-path/{my_param:int}'"
            )
        param_name, param_type = (p.strip() for p in param.split(":"))
        if not param_name:
            raise ImproperlyConfiguredException("Path parameter names should be of length greater than zero")
        if param_type not in param_type_map:
            raise ImproperlyConfiguredException(
                f"Path parameters should be declared with an allowed type, i.e. one of {','.join(param_type_map.keys())}"
            )

    @classmethod
    def _parse_path(cls, path: str) -> Tuple[str, str, List[Union[str, PathParameterDefinition]]]:
        """Normalize and parse a path.

        Splits the path into a list of components, parsing any that are path parameters. Also builds the OpenAPI
        compatible path, which does not include the type of the path parameters.

        Returns:
            A 3-tuple of the normalized path, the OpenAPI formatted path, and the list of parsed components.
        """
        path = normalize_path(path)

        parsed_components: List[Union[str, PathParameterDefinition]] = []
        path_format_components = []

        components = [component for component in path.split("/") if component]
        for component in components:
            param_match = param_match_regex.fullmatch(component)
            if param_match:
                param = param_match.group(1)
                cls._validate_path_parameter(param)
                param_name, param_type = (p.strip() for p in param.split(":"))
                type_class = param_type_map[param_type]
                parser = parsers_map[type_class] if type_class not in {str, Path} else None
                parsed_components.append(
                    PathParameterDefinition(name=param_name, type=type_class, full=param, parser=parser)
                )
                path_format_components.append("{" + param_name + "}")
            else:
                parsed_components.append(component)
                path_format_components.append(component)

        path_format = join_paths(path_format_components)

        return path, path_format, parsed_components
