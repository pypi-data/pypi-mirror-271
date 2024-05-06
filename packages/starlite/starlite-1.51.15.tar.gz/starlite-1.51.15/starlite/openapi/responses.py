from copy import copy
from http import HTTPStatus
from operator import attrgetter
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Optional, Tuple, Type

from pydantic_openapi_schema.v3_1_0 import Response
from pydantic_openapi_schema.v3_1_0.header import Header
from pydantic_openapi_schema.v3_1_0.media_type import (
    MediaType as OpenAPISchemaMediaType,
)
from pydantic_openapi_schema.v3_1_0.schema import Schema
from typing_extensions import get_args, get_origin

from starlite.datastructures.response_containers import File, Redirect, Stream, Template
from starlite.enums import MediaType
from starlite.exceptions import (
    HTTPException,
    ImproperlyConfiguredException,
    ValidationException,
)
from starlite.openapi.enums import OpenAPIFormat, OpenAPIType
from starlite.openapi.schema import create_schema
from starlite.openapi.utils import pascal_case_to_text
from starlite.response import Response as StarliteResponse
from starlite.signature.models import SignatureField
from starlite.utils import get_enum_string_value, get_name, is_class_and_subclass

if TYPE_CHECKING:
    from pydantic_openapi_schema.v3_1_0.responses import Responses

    from starlite.datastructures.cookie import Cookie
    from starlite.handlers import HTTPRouteHandler
    from starlite.plugins.base import PluginProtocol


def create_cookie_schema(cookie: "Cookie") -> Schema:
    """Given a Cookie instance, return its corresponding OpenAPI schema.

    Args:
        cookie: Cookie

    Returns:
        Schema
    """
    cookie_copy = copy(cookie)
    cookie_copy.value = "<string>"
    value = cookie_copy.to_header(header="")
    return Schema(description=cookie.description or "", example=value)


def create_success_response(
    route_handler: "HTTPRouteHandler", generate_examples: bool, plugins: List["PluginProtocol"]
) -> Response:
    """Create the schema for a success response."""
    signature = route_handler.signature
    default_descriptions: Dict[Any, str] = {
        Stream: "Stream Response",
        Redirect: "Redirect Response",
        File: "File Download",
    }
    description = (
        route_handler.response_description
        or default_descriptions.get(signature.return_annotation)
        or HTTPStatus(route_handler.status_code).description
    )

    if signature.return_annotation not in {signature.empty, None, Redirect, File, Stream}:
        return_annotation = signature.return_annotation
        if signature.return_annotation is Template:
            return_annotation = str  # since templates return str
            route_handler.media_type = get_enum_string_value(MediaType.HTML)
        elif is_class_and_subclass(get_origin(signature.return_annotation), StarliteResponse):
            return_annotation = get_args(signature.return_annotation)[0] or Any

        schema = create_schema(
            field=SignatureField.create(field_type=return_annotation),
            generate_examples=generate_examples,
            plugins=plugins,
        )
        schema.contentEncoding = route_handler.content_encoding
        schema.contentMediaType = route_handler.content_media_type
        response = Response(
            content={
                route_handler.media_type: OpenAPISchemaMediaType(
                    media_type_schema=schema,
                )
            },
            description=description,
        )

    elif signature.return_annotation is Redirect:
        response = Response(
            content=None,
            description=description,
            headers={
                "location": Header(
                    param_schema=Schema(type=OpenAPIType.STRING), description="target path for the redirect"
                )
            },
        )

    elif signature.return_annotation in (File, Stream):
        response = Response(
            content={
                route_handler.media_type: OpenAPISchemaMediaType(
                    media_type_schema=Schema(
                        type=OpenAPIType.STRING,
                        contentEncoding=route_handler.content_encoding or "application/octet-stream",
                        contentMediaType=route_handler.content_media_type,
                    ),
                )
            },
            description=description,
            headers={
                "content-length": Header(
                    param_schema=Schema(type=OpenAPIType.STRING), description="File size in bytes"
                ),
                "last-modified": Header(
                    param_schema=Schema(type=OpenAPIType.STRING, schema_format=OpenAPIFormat.DATE_TIME),
                    description="Last modified data-time in RFC 2822 format",
                ),
                "etag": Header(param_schema=Schema(type=OpenAPIType.STRING), description="Entity tag"),
            },
        )

    else:
        response = Response(
            content=None,
            description=description,
        )

    if response.headers is None:
        response.headers = {}

    for key, value in route_handler.resolve_response_headers().items():
        header = Header()
        for attribute_name, attribute_value in value.dict(exclude_none=True).items():
            if attribute_name == "value":
                header.param_schema = create_schema(
                    field=SignatureField.create(field_type=type(attribute_value)),
                    generate_examples=False,
                    plugins=plugins,
                )

            elif attribute_name != "documentation_only":
                setattr(header, attribute_name, attribute_value)
        response.headers[key] = header

    if cookies := route_handler.resolve_response_cookies():
        response.headers["Set-Cookie"] = Header(
            param_schema=Schema(
                allOf=[create_cookie_schema(cookie=cookie) for cookie in sorted(cookies, key=attrgetter("key"))]
            )
        )

    return response


def create_error_responses(exceptions: List[Type[HTTPException]]) -> Iterator[Tuple[str, Response]]:
    """Create the schema for error responses, if any."""
    grouped_exceptions: Dict[int, List[Type[HTTPException]]] = {}
    for exc in exceptions:
        if not grouped_exceptions.get(exc.status_code):
            grouped_exceptions[exc.status_code] = []
        grouped_exceptions[exc.status_code].append(exc)
    for status_code, exception_group in grouped_exceptions.items():
        exceptions_schemas = [
            Schema(
                type=OpenAPIType.OBJECT,
                required=["detail", "status_code"],
                properties={
                    "status_code": Schema(type=OpenAPIType.INTEGER),
                    "detail": Schema(type=OpenAPIType.STRING),
                    "extra": Schema(
                        type=[OpenAPIType.NULL, OpenAPIType.OBJECT, OpenAPIType.ARRAY], additionalProperties=Schema()
                    ),
                },
                description=pascal_case_to_text(get_name(exc)),
                examples=[{"status_code": status_code, "detail": HTTPStatus(status_code).phrase, "extra": {}}],
            )
            for exc in exception_group
        ]
        if len(exceptions_schemas) > 1:
            schema = Schema(oneOf=exceptions_schemas)  # type:ignore[arg-type]
        else:
            schema = exceptions_schemas[0]
        yield str(status_code), Response(
            description=HTTPStatus(status_code).description,
            content={MediaType.JSON: OpenAPISchemaMediaType(media_type_schema=schema)},
        )


def create_additional_responses(
    route_handler: "HTTPRouteHandler", plugins: List["PluginProtocol"]
) -> Iterator[Tuple[str, Response]]:
    """Create the schema for additional responses, if any."""
    if not route_handler.responses:
        return

    for status_code, additional_response in route_handler.responses.items():
        schema = create_schema(
            field=SignatureField.create(field_type=additional_response.model),
            generate_examples=additional_response.generate_examples,
            plugins=plugins,
        )
        yield str(status_code), Response(
            description=additional_response.description,
            content={additional_response.media_type: OpenAPISchemaMediaType(media_type_schema=schema)},
        )


def create_responses(
    route_handler: "HTTPRouteHandler",
    raises_validation_error: bool,
    generate_examples: bool,
    plugins: List["PluginProtocol"],
) -> Optional["Responses"]:
    """Create a Response model embedded in a `Responses` dictionary for the given RouteHandler or return None."""

    responses: "Responses" = {
        str(route_handler.status_code): create_success_response(
            route_handler=route_handler,
            generate_examples=generate_examples,
            plugins=plugins,
        ),
    }

    exceptions = route_handler.raises or []
    if raises_validation_error and ValidationException not in exceptions:
        exceptions.append(ValidationException)
    for status_code, response in create_error_responses(exceptions=exceptions):
        responses[status_code] = response

    for status_code, response in create_additional_responses(route_handler, plugins):
        if status_code in responses:
            raise ImproperlyConfiguredException(
                f"Additional response for status code {status_code} already exists in success or error responses"
            )

        responses[status_code] = response

    return responses or None
