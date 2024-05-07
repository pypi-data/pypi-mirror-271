from typing import Optional, Union

# "Literal" is only available on Python 3.8
# and above, so for older versions of Python
# we use "typing_extensions" instead.
# (https://stackoverflow.com/questions/61206437/importerror-cannot-import-name-literal-from-typing)
try:
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal
from uuid import UUID

from pydantic import Field, BaseModel

from bodosdk.base import APIBaseModel


class CreateAwsProviderDataAPIModel(APIBaseModel):
    tf_backend_region: str = Field(..., alias="tfBackendRegion")
    secret_access_key: Optional[str] = Field(None, alias="secretAccessKey")
    access_key_id: Optional[str] = Field(None, alias="accessKeyId")


class CreateAzureProviderDataAPIModel(APIBaseModel):
    tf_backend_region: Optional[str] = Field(None, alias="tfBackendRegion")
    subscription_id: str = Field(..., alias="subscriptionId")
    tenant_id: str = Field(..., alias="tenantId")
    resource_group: str = Field(..., alias="resourceGroup")


class CreateAwsCloudConfigAPIModel(APIBaseModel):
    cloud_provider: Optional[Literal["AWS"]] = Field("AWS", alias="cloudProvider")
    name: Optional[str]
    data: Optional[CreateAwsProviderDataAPIModel] = Field(..., alias="awsProviderData")


class CreateAzureCloudConfigAPIModel(APIBaseModel):
    cloud_provider: Optional[Literal["AZURE"]] = Field("AZURE", alias="cloudProvider")
    name: Optional[str]
    data: Optional[CreateAzureProviderDataAPIModel] = Field(
        ..., alias="azureProviderData"
    )


class AwsProviderDataAPIModel(CreateAwsProviderDataAPIModel):
    tf_bucket_name: Optional[str] = Field(None, alias="tfBucketName")
    tf_dynamo_db_table_name: Optional[str] = Field(None, alias="tfDynamoDBTableName")
    role_arn: Optional["str"] = Field(None, alias="RoleArn")
    external_id: Optional[str] = Field(None, alias="externalId")
    account_id: Optional[str] = Field(None, alias="accountId")


class AzureProviderDataAPIModel(CreateAzureProviderDataAPIModel):
    application_id: str = Field(..., alias="applicationId")


class AwsCloudConfigAPIModel(CreateAwsCloudConfigAPIModel):
    uuid: Union[str, UUID]
    status: Optional[str]
    organization_uuid: Optional[Union[str, UUID]] = Field(..., alias="organizationUUID")


class AzureCloudConfigAPIModel(CreateAzureCloudConfigAPIModel):
    uuid: Union[str, UUID]
    status: Optional[str]
    organization_uuid: Optional[Union[str, UUID]] = Field(..., alias="organizationUUID")


class CloudConfigAPIModel(BaseModel):
    __root__: Union[AzureCloudConfigAPIModel, AwsCloudConfigAPIModel]
