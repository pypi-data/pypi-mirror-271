from typing import Optional, Union

from bodosdk import _version
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.interfaces import IBodoWorkspaceClient, ICatalogClient
from bodosdk.models import Catalog
from bodosdk.models.catalog import SnowflakeDetails, CatalogList


class CatalogClient(ICatalogClient):
    _deprecated_methods: dict

    def __init__(self, workspace_client: IBodoWorkspaceClient):
        self._workspace_client = workspace_client
        self._check_deprecation()

    def _check_deprecation(self):
        methods = self._workspace_client._sdk_api.get_catalog_client_info(
            _version.get_versions().get("version")
        )
        if isinstance(methods, dict) and methods:
            self._deprecated_methods = methods
        else:
            self._deprecated_methods = {}

    @property
    def Catalog(self) -> Catalog:
        return Catalog(self._workspace_client)

    @property
    def CatalogList(self) -> CatalogList:
        return CatalogList(self._workspace_client)

    @check_deprecation
    def list(self, filters: dict = None) -> CatalogList:
        return self.CatalogList(filters=filters)

    @check_deprecation
    def get(
        self,
        id: str,
    ) -> Catalog:
        return self.Catalog(uuid=id)._load()

    @check_deprecation
    def create(
        self,
        name: str,
        catalog_type: str,
        details: Union[SnowflakeDetails, dict],
        description: Optional[str] = None,
    ):
        if isinstance(details, dict) and catalog_type == "SNOWFLAKE":
            details = SnowflakeDetails(**details)
        catalog = self.Catalog(
            catalog_type=catalog_type,
            name=name,
            description=description,
            details=details,
        )
        return catalog._save()

    @check_deprecation
    def create_snowflake_catalog(
        self,
        name: str,
        details: Union[SnowflakeDetails, dict],
        description: Optional[str] = None,
    ):
        return self.create(name, "SNOWFLAKE", details, description)

    @check_deprecation
    def delete(self, id: str):
        self.Catalog(uuid=id).delete()
