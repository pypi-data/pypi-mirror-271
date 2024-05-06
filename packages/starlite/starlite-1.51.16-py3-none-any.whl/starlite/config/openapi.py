from typing import Dict, List, Literal, Optional, Set, Type, Union, cast

from pydantic import AnyUrl, BaseModel
from pydantic_openapi_schema.v3_1_0 import (
    Components,
    Contact,
    ExternalDocumentation,
    Info,
    License,
    OpenAPI,
    PathItem,
    Reference,
    SecurityRequirement,
    Server,
    Tag,
)

from starlite.openapi.controller import OpenAPIController


class OpenAPIConfig(BaseModel):
    """Configuration for OpenAPI.

    To enable OpenAPI schema generation and serving, pass an instance of this class to the
    :class:`Starlite <starlite.app.Starlite>` constructor using the 'openapi_config' kwargs.
    """

    create_examples: bool = False
    """Generate examples using the pydantic-factories library."""
    openapi_controller: Type[OpenAPIController] = OpenAPIController
    """Controller for generating OpenAPI routes.

    Must be subclass of :class:`OpenAPIController <starlite.openapi.controller.OpenAPIController>`.
    """
    title: str
    """Title of API documentation."""
    version: str
    """API version, e.g. '1.0.0'."""
    contact: Optional[Contact] = None
    """API contact information, should be an :class:`Contact <pydantic_openapi_schema.v3_1_0.contact.Contact>` instance."""
    description: Optional[str] = None
    """API description."""
    external_docs: Optional[ExternalDocumentation] = None
    """Links to external documentation.

    Should be an instance of :class:`ExternalDocumentation <pydantic_openapi_schema.v3_1_0.external_documentation.ExternalDocumentation>`.
    """
    license: Optional[License] = None
    """API Licensing information.

    Should be an instance of :class:`License <pydantic_openapi_schema.v3_1_0.license.License>`.
    """
    security: Optional[List[SecurityRequirement]] = None
    """API Security requirements information.

    Should be an instance of :class:`SecurityRequirement <pydantic_openapi_schema.v3_1_0.security_requirement.SecurityRequirement>`.
    """
    components: Optional[Union[Components, List[Components]]] = None
    """API Components information.

    Should be an instance of :class:`Components <pydantic_openapi_schema.v3_10_0.components.Components>` or a list thereof.
    """
    servers: List[Server] = [Server(url="/")]
    """A list of :class:`Server <pydantic_openapi_schema.v3_1_0.server.Server>` instances."""
    summary: Optional[str] = None
    """A summary text."""
    tags: Optional[List[Tag]] = None
    """A list of :class:`Tag <pydantic_openapi_schema.v3_1_0.tag.Tag>` instances."""
    terms_of_service: Optional[AnyUrl] = None
    """URL to page that contains terms of service."""
    use_handler_docstrings: bool = False
    """Draw operation description from route handler docstring if not otherwise provided."""
    webhooks: Optional[Dict[str, Union[PathItem, Reference]]] = None
    """A mapping of key to either :class:`PathItem <pydantic_openapi_schema.v3_1_0.path_item.PathItem>` or.

    :class:`Reference <pydantic_openapi_schema.v3_1_0.reference.Reference>` objects.
    """
    root_schema_site: Literal["redoc", "swagger", "elements"] = "redoc"
    """The static schema generator to use for the "root" path of `/schema/`."""
    enabled_endpoints: Set[str] = {"redoc", "swagger", "elements", "openapi.json", "openapi.yaml"}
    """A set of the enabled documentation sites and schema download endpoints."""
    by_alias: bool = True
    """Render pydantic model schema using field aliases, if defined."""

    def to_openapi_schema(self) -> "OpenAPI":
        """Return an ``OpenAPI`` instance from the values stored in ``self``.

        Returns:
            An instance of :class:`OpenAPI <pydantic_openapi_schema.v3_1_0.open_api.OpenAPI>`.
        """

        if isinstance(self.components, list):
            merged_components = Components()
            for components in self.components:
                for key in components.__fields__:
                    value = getattr(components, key, None)
                    if value:
                        merged_value_dict = getattr(merged_components, key, {}) or {}
                        merged_value_dict.update(value)
                        setattr(merged_components, key, merged_value_dict)
            self.components = merged_components

        return OpenAPI(
            externalDocs=self.external_docs,
            security=self.security,
            components=cast("Components", self.components),
            servers=self.servers,
            tags=self.tags,
            webhooks=self.webhooks,
            info=Info(
                title=self.title,
                version=self.version,
                description=self.description,
                contact=self.contact,
                license=self.license,
                summary=self.summary,
                termsOfService=self.terms_of_service,
            ),
            paths={},
        )
