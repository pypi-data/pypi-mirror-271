from datetime import date
from typing import Optional, List, Union, Dict
from uuid import UUID

from pydantic import Field

from bodosdk.api.models.base import BodoRole
from bodosdk.base import APIBaseModel
from bodosdk.api.base import PageMetadata


class CreateUpdateNotebookConfig(APIBaseModel):
    instance_type: Optional[str] = Field(..., alias="instanceType")
    image_version: Optional[str] = Field(..., alias="imageVersion")


class NetworkData(APIBaseModel):
    region: str
    storage_endpoint: bool = Field(..., alias="storageEndpoint")


class AWSNetworkData(NetworkData):
    vpc_id: Optional[str] = Field(None, alias="vpcId")
    fetched_vpc_id: Optional[str] = Field(None, alias="fetchedVpcId")
    public_subnets_ids: Optional[List[str]] = Field(None, alias="publicSubnetsIds")
    private_subnets_ids: Optional[List[str]] = Field(None, alias="privateSubnetsIds")
    policies_arn: Optional[List[str]] = Field(None, alias="policyArns")


class Relation(APIBaseModel):
    uuid: Union[UUID, str]


class WorkspaceAPIModel(APIBaseModel):
    name: Optional[str]
    uuid: Optional[UUID]
    status: Optional[str]
    organization_uuid: Optional[UUID] = Field(None, alias="organizationUUID")
    network_data: Optional[Union[AWSNetworkData, NetworkData]] = Field(
        None, alias="networkData"
    )
    created_by: Optional[str] = Field(None, alias="createdBy")
    assigned_at: Optional[date] = Field(None, alias="assignedAt")
    custom_tags: Optional[Dict] = Field(None, alias="customTags")
    jupyter_last_activity: Optional[date] = Field(None, alias="jupterLastActivity")
    jupyter_is_active: Optional[bool] = Field(False, alias="jupyterIsActive")
    cloud_config: Optional[Relation] = Field(None, alias="cloudConfig")


class WorkspaceListAPIModel(APIBaseModel):
    data: List[WorkspaceAPIModel]
    metadata: PageMetadata


class UserAssignment(APIBaseModel):
    class Config:
        use_enum_values = True

    email: str
    skip_email: bool = Field(..., alias="skipEmail")
    bodo_role: BodoRole = Field(..., alias="bodoRole")
