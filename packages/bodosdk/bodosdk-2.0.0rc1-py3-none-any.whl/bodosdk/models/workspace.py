from __future__ import annotations

import time
from datetime import datetime
from typing import Optional, Union, Dict, Any, Iterator, List
from uuid import uuid4, UUID

from pydantic import Field

from bodosdk.api.models.workspace import (
    WorkspaceAPIModel,
)
from bodosdk.base import SDKBaseModel
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.exceptions import TimeoutException, ResourceNotFound, ValidationError
from bodosdk.interfaces import (
    IWorkspace,
    IWorkspaceList,
    IWorkspaceFilter,
    IBodoOrganizationClient,
)
from bodosdk.models import AwsCloudConfig, AzureCloudConfig
from bodosdk.models.common import NetworkData, AWSNetworkData


class Workspace(SDKBaseModel, IWorkspace):
    name: Optional[str]
    uuid: Optional[Union[str, UUID]]
    status: Optional[str]
    organization_uuid: Optional[Union[str, UUID]] = Field(
        None, alias="organizationUUID"
    )
    network_data: Optional[Union[NetworkData, AWSNetworkData]] = Field(
        None, alias="networkData"
    )
    created_by: Optional[str] = Field(None, alias="createdBy")
    notebook_auto_deploy_enabled: Optional[bool] = Field(
        None, alias="notebookAutoDeployEnabled"
    )
    assigned_at: Optional[datetime] = Field(None, alias="assignedAt")
    custom_tags: Optional[Dict[str, Any]] = Field(
        default_factory=dict, alias="customTags"
    )
    jupyter_last_activity: Optional[datetime] = Field(None, alias="jupyterLastActivity")
    jupyter_is_active: Optional[bool] = Field(False, alias="jupyterIsActive")
    cloud_config: Optional[Union[AwsCloudConfig, AzureCloudConfig]] = Field(
        None, alias="cloudConfig"
    )

    @property
    def id(self):
        return self.uuid

    def __init__(self, org_client: IBodoOrganizationClient = None, **data):
        """
        Initializes a new Workspqce model.

        Args:
            org_client: An optional client for interacting with the workspace API.
            **data: Arbitrary keyword arguments representing workspace properties.
        """
        super().__init__(**data)
        self._org_client = org_client

    def __call__(self, **data) -> Workspace:
        """
        Creates a new workspace with the same workspace client and provided data.

        Args:
            **data: Arbitrary keyword arguments representing workspace properties.

        Returns:
            A new instance of Workspace.
        """
        return Workspace(self._org_client, **data)

    def __setattr__(self, key: str, value: Any):
        """
        Sets the value of an attribute using custom logic for cloud_config,
        ensuring they are correctly instantiated.

        Args:
            key: The name of the attribute to set.
            value: The value to assign to the attribute.

        Raises:
            ValueError: If provided data for 'cloud_config' is invalid.
        """
        if key == "cloud_config" and isinstance(value, dict):
            try:
                instance_role_value = self._org_client.CloudConfig(**value)
                super().__setattr__(key, instance_role_value)
            except ValidationError as e:
                raise ValueError(f"Invalid data for CloudConfig: {e}")
        elif key == "network_data" and isinstance(value, dict):
            try:
                instance_role_value = (
                    AWSNetworkData(**value)
                    if "vpc_id" in value
                    else NetworkData(**value)
                )
                super().__setattr__(key, instance_role_value)
            except ValidationError as e:
                raise ValueError(f"Invalid data for network_data: {e}")
        else:
            super().__setattr__(key, value)

    @check_deprecation
    def _save(self) -> Workspace:
        if self._modified:
            if self.id:
                return self
            else:
                self._mutable = True
                self.name = self.name if self.name else f"Workspace  {uuid4()}"
                self._mutable = False
                result = self._org_client._workspace_api.create(
                    WorkspaceAPIModel(**self.dict())
                )
            self._update(result.dict())
        return self

    @check_deprecation
    def _load(self) -> Workspace:
        """
        Loads the current state of the WorkspaceAPIModel from the workspace API.

        Returns:
            The updated Workspace.
        """
        resp = self._org_client._workspace_api.get(self.id)
        self._update(resp.dict())
        self._modified = False
        return self

    @check_deprecation
    def delete(self) -> Workspace:
        """
        Deletes the workspace from the API based on its UUID and updates the instance's properties
        with the response from the deletion API call.

        Returns:
            The Workspace instance after deletion, updated with the API's response data.
        """

        resp = self._org_client._workspace_api.remove(self.id)
        self._update(resp.dict())
        self._modified = False
        return self

    @check_deprecation
    def wait_for_status(self, statuses, timeout=600, tick=30) -> Workspace:
        """
        Waits for the workspace to reach one of the specified states within a given timeout.

        Args:
            statuses: A list of states to wait for.
            timeout: The maximum time to wait before raising a TimeoutException.
            tick: The interval between checks.

        Returns:
            The workspace instance, once it has reached one of the desired states.

        Raises:
            TimeoutException: If the workspace does not reach a desired state within the timeout.
        """
        if "FAILED" not in statuses:
            statuses.append("FAILED")
        try:
            self._load()
        except ResourceNotFound:  # If resource not found then workspace is TERMINATED
            if "TERMINATED" in statuses:
                self._mutable = True
                self.status = "TERMINATED"
                self._mutable = False
                return self
            raise
        start_time = time.time()  # Record the start time
        while self.status not in statuses:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self._load()

            # Check if timeout is reached
            if elapsed_time > timeout:
                raise TimeoutException(
                    f"workspace {self.uuid} wait for states {statuses} timeout! Current state: {self.status}"
                )
            time.sleep(tick)
        return self

    @check_deprecation
    def update_infra(self) -> Workspace:
        self._org_client._workspace_api.update_infra(self)
        return self


class WorkspaceFilter(SDKBaseModel, IWorkspaceFilter):
    class Config:
        extra = "forbid"
        allow_population_by_field_name = True

    ids: Optional[List[str]] = Field(default_factory=list, alias="uuids")
    names: Optional[List[str]] = Field(default_factory=list, alias="names")
    statuses: Optional[List[str]] = Field(default_factory=list, alias="statuses")
    organization_uuids: Optional[List[str]] = Field(
        default_factory=list, alias="organizationUUIDs"
    )


class WorkspaceList(IWorkspaceList, SDKBaseModel):
    class Config:
        extra = "forbid"
        allow_population_by_field_name = True

    page: Optional[int] = Field(0, alias="page")
    page_size: Optional[int] = Field(10, alias="pageSize")
    total: Optional[int] = Field(None, alias="total")
    order: Optional[Dict] = Field(default_factory=dict, alias="order")
    filters: Optional[WorkspaceFilter] = Field(None, alias="filters")

    def __init__(self, org_client: IBodoOrganizationClient = None, **data):
        super().__init__(**data)
        self._elements: List[IWorkspace] = []
        self._org_client = org_client

    def __call__(self, **data) -> WorkspaceList:
        if data.get("filters") and isinstance(data.get("filters"), dict):
            data["filters"] = WorkspaceFilter(**data["filters"])
        workspace_list = WorkspaceList(self._org_client, **data)
        return workspace_list._load_next_page()

    def __iter__(self) -> Iterator[Workspace]:
        yield from super().__iter__()

    def _load_next_page(self) -> WorkspaceList:
        self._mutable = True
        self.page += 1
        resp = self._org_client._workspace_api.list(
            page=self.page,
            page_size=self.page_size,
            uuids=self.filters.ids if self.filters else None,
            statuses=self.filters.statuses if self.filters else None,
            names=self.filters.names if self.filters else None,
        )
        for workspace_data in resp.data:
            workspace = Workspace(**workspace_data.dict(), org_client=self._org_client)
            self._elements.append(workspace)
        self.total = resp.metadata.total_items
        self._mutable = False
        return self

    def __len__(self) -> int:
        return len(self._elements)

    def __getitem__(self, key) -> Union[Workspace, List[Workspace]]:
        return self._elements[key]

    def __contains__(self, obj) -> bool:
        return obj in self._elements

    @check_deprecation
    def delete(self) -> WorkspaceList:
        """
        Deletes the workspaces present on the list

        Returns:
            WorkspaceListAPIModel
        """
        for workspace in self._elements:
            workspace.delete()
        return self

    @check_deprecation
    def update_infra(self) -> WorkspaceList:
        for workspace in self._elements:
            workspace.update_infra()
        return self
