from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode

from httpx._content import encode_json as httpx_encode_json
from httpx._content import encode_multipart_data, encode_urlencoded_data
from httpx._types import FileTypes  # noqa: TC002
from pydantic import BaseModel

from starlite.app import Starlite
from starlite.connection import Request
from starlite.enums import HttpMethod, ParamType, RequestEncodingType, ScopeType
from starlite.handlers.http import get
from starlite.types import HTTPScope, RouteHandlerType
from starlite.types.asgi_types import ASGIVersion
from starlite.utils.serialization import decode_json, encode_json

if TYPE_CHECKING:
    from starlite.datastructures.cookie import Cookie
    from starlite.handlers import HTTPRouteHandler


def _create_default_route_handler() -> "HTTPRouteHandler":
    @get("/")
    def _default_route_handler() -> None:
        ...

    return _default_route_handler


def _create_default_app() -> Starlite:
    return Starlite(route_handlers=[_create_default_route_handler()])


class RequestFactory:
    """Factory to create :class:`Request <starlite.connection.Request>` instances."""

    def __init__(
        self,
        app: Optional[Starlite] = None,
        server: str = "test.org",
        port: int = 3000,
        root_path: str = "",
        scheme: str = "http",
    ) -> None:
        """Initialize ``RequestFactory``

        Args:
             app: An instance of :class:`Starlite <starlite.app.Starlite>` to set as ``request.scope["app"]``.
             server: The server's domain.
             port: The server's port.
             root_path: Root path for the server.
             scheme: Scheme for the server.

        Examples:
            .. code-block: python

                from starlite import RequestEncodingType, Starlite, RequestFactory

                from tests import PersonFactory

                my_app = Starlite(route_handlers=[])
                my_server = "starlite.org"

                # Create a GET request
                query_params = {"id": 1}
                get_user_request = RequestFactory(app=my_app, server=my_server).get(
                    "/person", query_params=query_params
                )

                # Create a POST request
                new_person = PersonFactory.build()
                create_user_request = RequestFactory(app=my_app, server=my_server).post(
                    "/person", data=person
                )

                # Create a request with a special header
                headers = {"header1": "value1"}
                request_with_header = RequestFactory(app=my_app, server=my_server).get(
                    "/person", query_params=query_params, headers=headers
                )

                # Create a request with a media type
                request_with_media_type = RequestFactory(app=my_app, server=my_server).post(
                    "/person", data=person, request_media_type=RequestEncodingType.MULTI_PART
                )

        """

        self.app = app if app is not None else _create_default_app()
        self.server = server
        self.port = port
        self.root_path = root_path
        self.scheme = scheme

    def _create_scope(
        self,
        path: str,
        http_method: HttpMethod,
        session: Optional[Dict[str, Any]] = None,
        user: Any = None,
        auth: Any = None,
        query_params: Optional[Dict[str, Union[str, List[str]]]] = None,
        state: Optional[Dict[str, Any]] = None,
        path_params: Optional[Dict[str, str]] = None,
        http_version: Optional[str] = "1.1",
        route_handler: Optional[RouteHandlerType] = None,
    ) -> HTTPScope:
        """Create the scope for the :class:`Request <starlite.connection.Request>`.

        Args:
            path: The request's path.
            http_method: The request's HTTP method.
            session: A dictionary of session data.
            user: A value for `request.scope["user"]`.
            auth: A value for `request.scope["auth"]`.
            query_params: A dictionary of values from which the request's query will be generated.
            state: Arbitrary request state.
            path_params: A string keyed dictionary of path parameter values.
            http_version: HTTP version. Defaults to "1.1".
            route_handler: A route handler instance or method. If not provided a default handler is set.

        Returns:
            A dictionary that can be passed as a scope to the :class:`Request <starlite.connection.Request>` ctor.
        """
        if session is None:
            session = {}

        if state is None:
            state = {}

        if path_params is None:
            path_params = {}

        return HTTPScope(
            type=ScopeType.HTTP,
            method=http_method.value,
            scheme=self.scheme,
            server=(self.server, self.port),
            root_path=self.root_path.rstrip("/"),
            path=path,
            headers=[],
            app=self.app,
            session=session,
            user=user,
            auth=auth,
            query_string=urlencode(query_params, doseq=True).encode() if query_params else b"",
            path_params=path_params,
            client=(self.server, self.port),
            state=state,
            asgi=ASGIVersion(spec_version="3.0", version="3.0"),
            http_version=http_version or "1.1",
            raw_path=path.encode("ascii"),
            route_handler=route_handler or _create_default_route_handler(),
            extensions={},
        )

    @classmethod
    def _create_cookie_header(
        cls, headers: Dict[str, str], cookies: Optional[Union[List["Cookie"], str]] = None
    ) -> None:
        """Create the cookie header and add it to the ``headers`` dictionary.

        Args:
            headers: A dictionary of headers, the cookie header will be added to it.
            cookies: A string representing the cookie header or a list of "Cookie" instances.
                This value can include multiple cookies.
        """
        if not cookies:
            return

        if isinstance(cookies, list):
            cookie_header = "; ".join(cookie.to_header(header="") for cookie in cookies)
            headers[ParamType.COOKIE] = cookie_header
        elif isinstance(cookies, str):
            headers[ParamType.COOKIE] = cookies

    def _build_headers(
        self,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Union[List["Cookie"], str]] = None,
    ) -> List[Tuple[bytes, bytes]]:
        """Build a list of encoded headers that can be passed to the request scope.

        Args:
            headers: A dictionary of headers.
            cookies: A string representing the cookie header or a list of "Cookie" instances.
                This value can include multiple cookies.

        Returns:
            A list of encoded headers that can be passed to the request scope.
        """
        headers = headers or {}
        self._create_cookie_header(headers, cookies)
        return [
            ((key.lower()).encode("latin-1", errors="ignore"), value.encode("latin-1", errors="ignore"))
            for key, value in headers.items()
        ]

    def _create_request_with_data(
        self,
        http_method: HttpMethod,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Union[List["Cookie"], str]] = None,
        session: Optional[Dict[str, Any]] = None,
        user: Any = None,
        auth: Any = None,
        request_media_type: RequestEncodingType = RequestEncodingType.JSON,
        data: Optional[Union[Dict[str, Any], "BaseModel"]] = None,
        files: Optional[Union[Dict[str, FileTypes], List[Tuple[str, FileTypes]]]] = None,
        query_params: Optional[Dict[str, Union[str, List[str]]]] = None,
        state: Optional[Dict[str, Any]] = None,
        path_params: Optional[Dict[str, str]] = None,
        http_version: Optional[str] = "1.1",
        route_handler: Optional[RouteHandlerType] = None,
    ) -> Request[Any, Any]:
        """Create a :class:`Request <starlite.connection.Request>` instance that has body (data)

        Args:
            http_method: The request's HTTP method.
            path: The request's path.
            headers: A dictionary of headers.
            cookies: A string representing the cookie header or a list of "Cookie" instances.
                This value can include multiple cookies.
            session: A dictionary of session data.
            user: A value for `request.scope["user"]`
            auth: A value for `request.scope["auth"]`
            request_media_type: The 'Content-Type' header of the request.
            data: A value for the request's body. Can be either a pydantic model instance
                or a string keyed dictionary.
            query_params: A dictionary of values from which the request's query will be generated.
            state: Arbitrary request state.
            path_params: A string keyed dictionary of path parameter values.
            http_version: HTTP version. Defaults to "1.1".
            route_handler: A route handler instance or method. If not provided a default handler is set.

        Returns:
            A :class:`Request <starlite.connection.Request>` instance
        """
        scope = self._create_scope(
            path=path,
            http_method=http_method,
            session=session,
            user=user,
            auth=auth,
            query_params=query_params,
            state=state,
            path_params=path_params,
            http_version=http_version,
            route_handler=route_handler,
        )

        headers = headers or {}
        if data:
            if isinstance(data, BaseModel):
                data = data.dict()
            if request_media_type == RequestEncodingType.JSON:
                encoding_headers, stream = httpx_encode_json(data)
            elif request_media_type == RequestEncodingType.MULTI_PART:
                encoding_headers, stream = encode_multipart_data(data, files=files or [], boundary=None)  # type: ignore[assignment]
            else:
                encoding_headers, stream = encode_urlencoded_data(decode_json(encode_json(data)))
            headers.update(encoding_headers)
            body = b""
            for chunk in stream:
                body += chunk
            scope["_body"] = body  # type: ignore[typeddict-unknown-key]
        self._create_cookie_header(headers, cookies)
        scope["headers"] = self._build_headers(headers)
        return Request(scope=scope)

    def get(
        self,
        path: str = "/",
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Union[List["Cookie"], str]] = None,
        session: Optional[Dict[str, Any]] = None,
        user: Any = None,
        auth: Any = None,
        query_params: Optional[Dict[str, Union[str, List[str]]]] = None,
        state: Optional[Dict[str, Any]] = None,
        path_params: Optional[Dict[str, str]] = None,
        http_version: Optional[str] = "1.1",
        route_handler: Optional[RouteHandlerType] = None,
    ) -> Request[Any, Any]:
        """Create a GET :class:`Request <starlite.connection.Request>` instance.

        Args:
            path: The request's path.
            headers: A dictionary of headers.
            cookies: A string representing the cookie header or a list of "Cookie" instances.
                This value can include multiple cookies.
            session: A dictionary of session data.
            user: A value for `request.scope["user"]`.
            auth: A value for `request.scope["auth"]`.
            query_params: A dictionary of values from which the request's query will be generated.
            state: Arbitrary request state.
            path_params: A string keyed dictionary of path parameter values.
            http_version: HTTP version. Defaults to "1.1".
            route_handler: A route handler instance or method. If not provided a default handler is set.

        Returns:
            A :class:`Request <starlite.connection.Request>` instance
        """
        scope = self._create_scope(
            path=path,
            http_method=HttpMethod.GET,
            session=session,
            user=user,
            auth=auth,
            query_params=query_params,
            state=state,
            path_params=path_params,
            http_version=http_version,
            route_handler=route_handler,
        )

        scope["headers"] = self._build_headers(headers, cookies)
        return Request(scope=scope)

    def post(
        self,
        path: str = "/",
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Union[List["Cookie"], str]] = None,
        session: Optional[Dict[str, Any]] = None,
        user: Any = None,
        auth: Any = None,
        request_media_type: RequestEncodingType = RequestEncodingType.JSON,
        data: Optional[Union[Dict[str, Any], "BaseModel"]] = None,
        query_params: Optional[Dict[str, Union[str, List[str]]]] = None,
        state: Optional[Dict[str, Any]] = None,
        path_params: Optional[Dict[str, str]] = None,
        http_version: Optional[str] = "1.1",
        route_handler: Optional[RouteHandlerType] = None,
    ) -> Request[Any, Any]:
        """Create a POST :class:`Request <starlite.connection.Request>` instance.

        Args:
            path: The request's path.
            headers: A dictionary of headers.
            cookies: A string representing the cookie header or a list of "Cookie" instances.
                This value can include multiple cookies.
            session: A dictionary of session data.
            user: A value for `request.scope["user"]`.
            auth: A value for `request.scope["auth"]`.
            request_media_type: The 'Content-Type' header of the request.
            data: A value for the request's body. Can be either a pydantic model instance
                or a string keyed dictionary.
            query_params: A dictionary of values from which the request's query will be generated.
            state: Arbitrary request state.
            path_params: A string keyed dictionary of path parameter values.
            http_version: HTTP version. Defaults to "1.1".
            route_handler: A route handler instance or method. If not provided a default handler is set.

        Returns:
            A :class:`Request <starlite.connection.Request>` instance
        """
        return self._create_request_with_data(
            auth=auth,
            cookies=cookies,
            data=data,
            headers=headers,
            http_method=HttpMethod.POST,
            path=path,
            query_params=query_params,
            request_media_type=request_media_type,
            session=session,
            user=user,
            state=state,
            path_params=path_params,
            http_version=http_version,
            route_handler=route_handler,
        )

    def put(
        self,
        path: str = "/",
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Union[List["Cookie"], str]] = None,
        session: Optional[Dict[str, Any]] = None,
        user: Any = None,
        auth: Any = None,
        request_media_type: RequestEncodingType = RequestEncodingType.JSON,
        data: Optional[Union[Dict[str, Any], "BaseModel"]] = None,
        query_params: Optional[Dict[str, Union[str, List[str]]]] = None,
        state: Optional[Dict[str, Any]] = None,
        path_params: Optional[Dict[str, str]] = None,
        http_version: Optional[str] = "1.1",
        route_handler: Optional[RouteHandlerType] = None,
    ) -> Request[Any, Any]:
        """Create a PUT :class:`Request <starlite.connection.Request>` instance.

        Args:
            path: The request's path.
            headers: A dictionary of headers.
            cookies: A string representing the cookie header or a list of "Cookie" instances.
                This value can include multiple cookies.
            session: A dictionary of session data.
            user: A value for `request.scope["user"]`.
            auth: A value for `request.scope["auth"]`.
            request_media_type: The 'Content-Type' header of the request.
            data: A value for the request's body. Can be either a pydantic model instance
                or a string keyed dictionary.
            query_params: A dictionary of values from which the request's query will be generated.
            state: Arbitrary request state.
            path_params: A string keyed dictionary of path parameter values.
            http_version: HTTP version. Defaults to "1.1".
            route_handler: A route handler instance or method. If not provided a default handler is set.

        Returns:
            A :class:`Request <starlite.connection.Request>` instance
        """
        return self._create_request_with_data(
            auth=auth,
            cookies=cookies,
            data=data,
            headers=headers,
            http_method=HttpMethod.PUT,
            path=path,
            query_params=query_params,
            request_media_type=request_media_type,
            session=session,
            user=user,
            state=state,
            path_params=path_params,
            http_version=http_version,
            route_handler=route_handler,
        )

    def patch(
        self,
        path: str = "/",
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Union[List["Cookie"], str]] = None,
        session: Optional[Dict[str, Any]] = None,
        user: Any = None,
        auth: Any = None,
        request_media_type: RequestEncodingType = RequestEncodingType.JSON,
        data: Optional[Union[Dict[str, Any], "BaseModel"]] = None,
        query_params: Optional[Dict[str, Union[str, List[str]]]] = None,
        state: Optional[Dict[str, Any]] = None,
        path_params: Optional[Dict[str, str]] = None,
        http_version: Optional[str] = "1.1",
        route_handler: Optional[RouteHandlerType] = None,
    ) -> Request[Any, Any]:
        """Create a PATCH :class:`Request <starlite.connection.Request>` instance.

        Args:
            path: The request's path.
            headers: A dictionary of headers.
            cookies: A string representing the cookie header or a list of "Cookie" instances.
                This value can include multiple cookies.
            session: A dictionary of session data.
            user: A value for `request.scope["user"]`.
            auth: A value for `request.scope["auth"]`.
            request_media_type: The 'Content-Type' header of the request.
            data: A value for the request's body. Can be either a pydantic model instance
                or a string keyed dictionary.
            query_params: A dictionary of values from which the request's query will be generated.
            state: Arbitrary request state.
            path_params: A string keyed dictionary of path parameter values.
            http_version: HTTP version. Defaults to "1.1".
            route_handler: A route handler instance or method. If not provided a default handler is set.

        Returns:
            A :class:`Request <starlite.connection.Request>` instance
        """
        return self._create_request_with_data(
            auth=auth,
            cookies=cookies,
            data=data,
            headers=headers,
            http_method=HttpMethod.PATCH,
            path=path,
            query_params=query_params,
            request_media_type=request_media_type,
            session=session,
            user=user,
            state=state,
            path_params=path_params,
            http_version=http_version,
            route_handler=route_handler,
        )

    def delete(
        self,
        path: str = "/",
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Union[List["Cookie"], str]] = None,
        session: Optional[Dict[str, Any]] = None,
        user: Any = None,
        auth: Any = None,
        query_params: Optional[Dict[str, Union[str, List[str]]]] = None,
        state: Optional[Dict[str, Any]] = None,
        path_params: Optional[Dict[str, str]] = None,
        http_version: Optional[str] = "1.1",
        route_handler: Optional[RouteHandlerType] = None,
    ) -> Request[Any, Any]:
        """Create a POST :class:`Request <starlite.connection.Request>` instance.

        Args:
            path: The request's path.
            headers: A dictionary of headers.
            cookies: A string representing the cookie header or a list of "Cookie" instances.
                This value can include multiple cookies.
            session: A dictionary of session data.
            user: A value for `request.scope["user"]`.
            auth: A value for `request.scope["auth"]`.
            query_params: A dictionary of values from which the request's query will be generated.
            state: Arbitrary request state.
            path_params: A string keyed dictionary of path parameter values.
            http_version: HTTP version. Defaults to "1.1".
            route_handler: A route handler instance or method. If not provided a default handler is set.

        Returns:
            A :class:`Request <starlite.connection.Request>` instance
        """
        scope = self._create_scope(
            path=path,
            http_method=HttpMethod.DELETE,
            session=session,
            user=user,
            auth=auth,
            query_params=query_params,
            state=state,
            path_params=path_params,
            http_version=http_version,
            route_handler=route_handler,
        )
        scope["headers"] = self._build_headers(headers, cookies)
        return Request(scope=scope)
