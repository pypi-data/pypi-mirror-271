from __future__ import annotations
from typing import Optional, Union, Any
from uuid import UUID

from pydantic import Field

from bodosdk.base import SDKBaseModel
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.exceptions import ValidationError
from bodosdk.interfaces import (
    IBodoOrganizationClient,
    ICloudConfig,
    ICloudConfigList,
    IAzureProviderData,
    IAwsProviderData,
    IAzureCloudConfig,
    IAwsCloudConfig,
)


class AzureProviderData(SDKBaseModel, IAzureProviderData):
    tf_backend_region: Optional[str] = Field(None, alias="tfBackendRegion")
    resource_group: Optional[str] = Field(None, alias="resourceGroup")
    subscription_id: Optional[str] = Field(None, alias="subscriptionId")
    tenant_id: Optional[str] = Field(None, alias="tenantId")
    tf_storage_account_name: Optional[str] = Field(None, alias="tfStorageAccountName")
    application_id: Optional[str] = Field(None, alias="applicationId")


class AwsProviderData(SDKBaseModel, IAwsProviderData):
    role_arn: Optional[str] = Field(None, alias="roleArn")
    tf_bucket_name: Optional[str] = Field(None, alias="tfBucketName")
    tf_dynamo_db_table_name: Optional[str] = Field(None, alias="tfDynamoDbTableName")
    tf_backend_region: Optional[str] = Field(None, alias="tfBackendRegion")
    external_id: Optional[str] = Field(None, alias="externalId")
    account_id: Optional[str] = Field(None, alias="accountId")


class CloudConfigBase(SDKBaseModel, ICloudConfig):
    cloud_provider: Optional[str] = Field(None, alias="cloudProvider")
    name: Optional[str]
    status: Optional[str]
    organization_uuid: Optional[str] = Field(None, alias="organizationUUID")
    custom_tags: Optional[dict] = Field(None, alias="customTags")
    uuid: Optional[Union[str, UUID]] = None
    data: Optional[Union[AwsProviderData, AzureProviderData]]

    def __init__(self, org_client: IBodoOrganizationClient = None, **data):
        """
        Initializes a new CloudConfig model.

        Args:
            org_client: An optional client for interacting with the CloudConfig API.
            **data: Arbitrary keyword arguments representing CloudConfig properties.
        """
        super().__init__(**data)
        self._org_client = org_client

    def __call__(self, **data) -> CloudConfigBase:
        """
        Creates a new CloudConfig with the same CloudConfig client and provided data.

        Args:
            **data: Arbitrary keyword arguments representing CloudConfig properties.

        Returns:
            A new instance of CloudConfig.
        """
        if data.get("cloud_provider", data.get("cloudProvider")) == "AWS":
            return AwsCloudConfig(self._org_client, **data)
        if data.get("cloud_provider", data.get("cloudProvider")) == "AZURE":
            return AzureCloudConfig(self._org_client, **data)
        return CloudConfigBase(self._org_client, **data)

    @property
    def id(self):
        return self.uuid

    @check_deprecation
    def _save(self) -> CloudConfigBase:
        if self._modified:
            if self.uuid:
                resp = self._org_client._cloud_config_api.update(self)
            else:
                resp = self._org_client._cloud_config_api.create(self)
            self._update(resp)
            self._modified = False
        return self

    @check_deprecation
    def _load(self) -> CloudConfigBase:
        resp = self._org_client._cloud_config_api.get(self.uuid)
        self._update(resp.dict())
        self._modified = False
        if self.cloud_provider == "AWS":
            return self._org_client.AwsCloudConfig(**self.dict())
        if self.cloud_provider == "AZURE":
            return self._org_client.AzureCloudConfig(**self.dict())

    @check_deprecation
    def delete(self):
        self._org_client._cloud_config_api.delete(self.uuid)

    def __setattr__(self, key: str, value: Any):
        if key == "data" and isinstance(value, dict):
            try:
                if self.cloud_provider == "AZURE":
                    super().__setattr__(key, AzureProviderData(**value))
                if self.cloud_provider == "AWS":
                    super().__setattr__(key, AwsProviderData(**value))
            except ValidationError as e:
                raise ValueError(f"Invalid data for data: {e}")
        else:
            super().__setattr__(key, value)


class AzureCloudConfig(CloudConfigBase, IAzureCloudConfig):
    data: Optional[AzureProviderData] = Field(None, alias="azureProviderData")

    def __call__(self, **data) -> CloudConfigBase:
        return AzureCloudConfig(self._org_client, **data)

    def __setattr__(self, key: str, value: Any):
        if key == "data" and isinstance(value, dict):
            try:
                super().__setattr__(key, AzureProviderData(**value))
            except ValidationError as e:
                raise ValueError(f"Invalid data for data: {e}")
        else:
            super().__setattr__(key, value)


class AwsCloudConfig(CloudConfigBase, IAwsCloudConfig):
    data: Optional[AwsProviderData] = Field(None, alias="awsProviderData")

    def __call__(self, **data) -> CloudConfigBase:
        return AwsCloudConfig(self._org_client, **data)

    def __setattr__(self, key: str, value: Any):
        if key == "data" and isinstance(value, dict):
            try:
                super().__setattr__(key, AwsProviderData(**value))
            except ValidationError as e:
                raise ValueError(f"Invalid data for data: {e}")
        else:
            super().__setattr__(key, value)


class CloudConfigList(ICloudConfigList, SDKBaseModel):
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
    filters: Optional[dict] = Field(None, alias="filters")

    def __init__(self, org_client: IBodoOrganizationClient = None, **data):
        super().__init__(**data)
        self._elements = []
        self._org_client = org_client

    def __call__(self, **data) -> CloudConfigList:
        cloud_config_list = CloudConfigList(self._org_client, **data)
        return cloud_config_list._load_next_page()

    def __iter__(self) -> Union[AwsCloudConfig, AzureCloudConfig]:
        yield from super().__iter__()

    def _load_next_page(self) -> CloudConfigList:
        self._mutable = True
        self.page += 1
        resp = self._org_client._cloud_config_api.list(
            page=self.page,
            page_size=self.page_size,
            provider=self.filters["providers]"] if self.filters else None,
            status=self.filters["statuses]"] if self.filters else None,
            # uuids=self.filters.ids if self.filters else None,
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
        for cc in resp:
            cloud_config = self._org_client.CloudConfig(**cc.dict())
            self._elements.append(cloud_config)
        self.total = len(resp)
        self._mutable = False
        return self

    @check_deprecation
    def delete(self):
        for cloud_config in self:
            cloud_config.delete()
