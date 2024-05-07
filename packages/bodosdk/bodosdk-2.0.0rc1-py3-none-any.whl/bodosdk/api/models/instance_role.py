from typing import Optional, List, Union

from pydantic import Field

from bodosdk.api.base import PageMetadata
from bodosdk.base import APIBaseModel


class InstanceRoleDataAPIModel(APIBaseModel):
    role_arn: str = Field(..., alias="roleArn")


class InstanceRoleApiModel(APIBaseModel):
    uuid: Optional[str] = Field(None, alias="uuid")
    name: str = Field(None, alias="name")
    data: Optional[Union[InstanceRoleDataAPIModel, dict]] = Field(None, alias="data")
    status: Optional[str] = Field(None, alias="status")
    description: Optional[str] = Field(None, alias="description")


class InstanceRoleListAPIModel(APIBaseModel):
    data: List[InstanceRoleApiModel]
    metadata: PageMetadata
