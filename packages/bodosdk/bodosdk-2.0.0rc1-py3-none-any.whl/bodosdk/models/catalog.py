from __future__ import annotations
from typing import Optional, Union, Any, List

from pydantic import Field

from bodosdk.base import SDKBaseModel
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.exceptions import ValidationError
from bodosdk.interfaces import (
    IBodoWorkspaceClient,
    ICatalog,
    ICatalogList,
    ICatalogFilter,
)


class SnowflakeDetails(SDKBaseModel):
    port: Optional[int]
    db_schema: Optional[str] = Field(None, aliast="schema")
    database: Optional[str]
    user_role: Optional[str] = Field(None, alias="userRole")
    username: Optional[str]
    warehouse: Optional[str]
    account_name: Optional[str] = Field(None, alias="accountName")
    password: Optional[str]


class Catalog(SDKBaseModel, ICatalog):
    uuid: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    catalog_type: Optional[str] = Field(None, alias="catalogType")
    details: Optional[Union[SnowflakeDetails, dict]] = None

    def __setattr__(self, key: str, value: Any):
        if key == "details" and isinstance(value, dict):
            try:
                super().__setattr__(key, SnowflakeDetails(**value))
            except ValidationError as e:
                raise ValueError(f"Invalid data for InstanceRole: {e}")
        else:
            super().__setattr__(key, value)

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        super().__init__(**data)
        self._workspace_client = workspace_client

    def __call__(self, **data) -> Catalog:
        return Catalog(self._workspace_client, **data)

    @check_deprecation
    def _save(self) -> Catalog:
        if self._modified:
            if self.uuid:
                resp = self._workspace_client._catalog_api.update(self)
            else:
                resp = self._workspace_client._catalog_api.create(self)
            self._update(resp)
            self._modified = False
        return self

    @check_deprecation
    def _load(self) -> Catalog:
        resp = self._workspace_client._catalog_api.get(self.uuid)
        self._update(resp.dict())
        self._modified = False
        return self

    @check_deprecation
    def delete(self):
        self._workspace_client._catalog_api.delete(self.uuid)


class CatalogFilter(SDKBaseModel, ICatalogFilter):
    names: Optional[List[str]]
    ids: Optional[List[str]]


class CatalogList(ICatalogList, SDKBaseModel):
    class Config:
        """
        Configuration for Pydantic models.
        https://docs.pydantic.dev/latest/api/config/
        """

        extra = "forbid"
        allow_population_by_field_name = True

    page: Optional[int] = Field(0, alias="page")
    page_size: Optional[int] = Field(10, alias="pageSize")
    total: Optional[int] = Field(None, alias="total")
    order: Optional[dict] = Field(default_factory=dict, alias="order")
    filters: Optional[Union[dict, CatalogFilter]] = Field(None, alias="filters")

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        super().__init__(**data)
        self._elements = []
        self._workspace_client = workspace_client

    def __call__(self, **data) -> CatalogList:
        catalog_list = CatalogList(self._workspace_client, **data)
        return catalog_list._load_next_page()

    def __iter__(self) -> Catalog:
        yield from super().__iter__()

    def _load_next_page(self) -> CatalogList:
        self._mutable = True
        self.page += 1
        resp = self._workspace_client._catalog_api.get_all(
            page=self.page,
            page_size=self.page_size,
            names=self.filters.names if self.filters else None,
            uuids=self.filters.ids if self.filters else None,
            order=self.order,
        )
        # self._deprecated_fields.update(
        #     resp.get("_deprecatedFields")
        #     if isinstance(resp.get("_deprecatedFields"), dict)
        #     else {}
        # )
        # self._deprecated_methods.update(
        #     resp._deprecated_methods
        #     if isinstance(resp._deprecated_methods, dict)
        #     else {}
        # )
        # if self.filters:
        #     self.filters._deprecated_fields.update(
        #         self._deprecated_fields.get("filters", {}).get("_deprecated_fields", {})
        #     )
        #     self.filters._deprecated_methods.update(
        #         self._deprecated_methods.get("filters", {}).get(
        #             "_deprecated_methods", {}
        #         )
        #     )
        for catalog_dict in resp:
            catalog = self._workspace_client.CatalogClient.Catalog(**catalog_dict)
            self._elements.append(catalog)
        self.total = len(resp)
        self._mutable = False
        return self

    @check_deprecation
    def delete(self):
        for catalog in self:
            catalog.delete()
