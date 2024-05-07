from __future__ import annotations
from typing import Optional, Union, List, Dict
from uuid import uuid4

from pydantic import Field

from bodosdk.api.models import InstanceRoleApiModel
from bodosdk.api.models.instance_role import InstanceRoleDataAPIModel
from bodosdk.base import SDKBaseModel
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.interfaces import (
    IInstanceRole,
    IBodoWorkspaceClient,
    IInstanceRoleList,
    IInstanceRoleFilter,
)


class InstanceRole(SDKBaseModel, IInstanceRole):
    uuid: Optional[str] = Field(None, alias="uuid")
    name: Optional[str] = Field(None, alias="name")
    description: Optional[str] = Field(None, alias="description")
    role_arn: Optional[str] = Field(None, alias="roleArn")
    status: Optional[str] = Field(None, alias="status")

    @property
    def id(self):
        return self.uuid

    def __init__(
        self, workspace_client: IBodoWorkspaceClient = None, **data
    ) -> InstanceRole:
        """
        Initializes a new InstaneRole.

        Args:
            workspace_client: An optional client for interacting with the workspace API.
            **data: Arbitrary keyword arguments representing cluster properties.
        """
        super().__init__(**data)
        self._workspace_client = workspace_client

    def __call__(self, **data) -> InstanceRole:
        """
        Creates a new instance role with the same workspace client and provided data.

        Args:
            **data: Arbitrary keyword arguments representing instance role properties.

        Returns:
            A new instance of InstaceRole.
        """
        return InstanceRole(self._workspace_client, **data)

    def _save(self) -> InstanceRole:
        if self._modified:
            if self.id:
                return self
            else:
                self._mutable = True
                self.name = self.name if self.name else f"Instance Role {uuid4()}"
                self._mutable = False
                existing_role = (
                    self._workspace_client.InstanceRoleClient.InstanceRoleList(
                        filters={"role_arns": [self.role_arn]}
                    )
                )
                if len(existing_role):
                    self = existing_role[0]
                    return self
                result = self._workspace_client._instance_api.create_role(
                    InstanceRoleApiModel(
                        name=self.name,
                        description=self.description,
                        data=InstanceRoleDataAPIModel(
                            role_arn=self.role_arn,
                        ),
                    )
                )
            self._update(
                {
                    "name": result.name,
                    "description": result.description,
                    "role_arn": result.data.role_arn,
                    "status": result.status,
                }
            )
        return self

    @check_deprecation
    def _load(self) -> InstanceRole:
        """
        Loads the current state of the Instance Role from the workspace.

        Returns:
            The updated InstanceRole.
        """
        resp = self._workspace_client._instance_api.get_role(self.id)
        mapped_response = resp.dict()
        mapped_response["role_arn"] = mapped_response["data"]["role_arn"]
        del mapped_response["data"]
        self._update(mapped_response)
        self._modified = False
        return self

    @check_deprecation
    def delete(self):
        """
        Removes instance role from workspace

        Returns:
            None
        """
        self._workspace_client._instance_api.remove_role(self.id)


class InstanceRoleFilter(SDKBaseModel, IInstanceRoleFilter):
    """
    Class representing filters for InstanceRoleList

    Attributes:
        ids: returns list matching given ids
        names: returns list matching given names
        role_arns: returns list matching giver arns

    """

    class Config:
        """
        Configuration for Pydantic models.
        https://docs.pydantic.dev/latest/api/config/
        """

        extra = "forbid"
        allow_population_by_field_name = True

    ids: Optional[List[str]] = Field(default_factory=list, alias="uuids")
    names: Optional[List[str]] = Field(default_factory=list, alias="names")
    role_arns: Optional[List[str]] = Field(default_factory=list, alias="roleArns")


class InstanceRoleList(IInstanceRoleList, SDKBaseModel):
    """
    Represents a list of instance roles within an SDK context, providing pagination and filtering capabilities.

    Attributes:
        page (Optional[int]): The current page number in the list of instance roles. Defaults to 0.
        page_size (Optional[int]): The number of instance roles to display per page. Defaults to 10.
        total (Optional[int]): The total number of instance roles available.
        order (Optional[Dict]): A dictionary specifying the order in which instance roles are sorted.
        filters (Optional[InstanceRoleFilter]): A filter object used to filter the instance roles listed.

    """

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
    order: Optional[Dict] = Field(default_factory=dict, alias="order")
    filters: Optional[InstanceRoleFilter] = Field(None, alias="filters")

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        """
        Initializes a new instance of InstanceRoleListAPIModel with optional parameters for
        configuration and a workspace client for API interactions.

        Args:
            workspace_client (IBodoWorkspaceClient, optional): The client used for workspace API calls.
                This client is responsible for fetching instance role data from the backend.
            **data: Arbitrary keyword arguments that can be used to set the values of the model fields
                upon initialization.
        """
        super().__init__(**data)
        self._elements = []
        self._workspace_client = workspace_client

    def __call__(self, **data) -> InstanceRoleList:
        """
        Creates and returns a new instance of InstanceRoleListAPIModel, optionally populated with
        the given data. This method is typically used for re-initializing or refreshing
        the list with new parameters or criteria.

        Args:
            **data: Arbitrary keyword arguments for configuring the new InstanceRoleListAPIModel instance.

        Returns:
            InstanceRoleList: A new instance of InstanceRoleListAPIModel with the given configuration.
        """
        instance_roles = InstanceRoleList(self._workspace_client, **data)
        return instance_roles._load_next_page()

    def __iter__(self) -> InstanceRole:
        """
        Provides an iterator over the instance roles in the list. It supports iteration
        through the instance roles, automatically loading the next page of instance roles when
        necessary.

        Returns:
            Iterator[IInstanceRole]: An iterator over the instance role objects in the list.
        """
        yield from super().__iter__()

    def _load_next_page(self) -> InstanceRoleList:
        """
        Loads the next page of instance roles from the workspace API, updating the internal
        list of instance roles and the total item count. This method modifies the instance
        in place and is usually called automatically during iteration or when accessing
        items beyond the current page.
        """
        self._mutable = True
        self.page += 1
        resp = self._workspace_client._instance_api.list(
            page=self.page,
            page_size=self.page_size,
            role_names=self.filters.names if self.filters else None,
            uuids=self.filters.ids if self.filters else None,
            role_arns=self.filters.role_arns if self.filters else None,
            order=self.order,
        )
        self._deprecated_fields.update(
            resp._deprecated_fields if isinstance(resp._deprecated_fields, dict) else {}
        )
        self._deprecated_methods.update(
            resp._deprecated_methods
            if isinstance(resp._deprecated_methods, dict)
            else {}
        )
        if self.filters:
            self.filters._deprecated_fields.update(
                self._deprecated_fields.get("filters", {}).get("_deprecated_fields", {})
            )
            self.filters._deprecated_methods.update(
                self._deprecated_methods.get("filters", {}).get(
                    "_deprecated_methods", {}
                )
            )
        for i in resp.data:
            instance = self._workspace_client.InstanceRoleClient.InstanceRole(
                **i.dict()
            )
            instance._update({"role_arn": i.data.role_arn})
            self._elements.append(instance)
        self.total = resp.metadata.total_items
        self._mutable = False
        return self

    def __len__(self) -> int:
        """
        Returns the total number of instance roles available across all pages, according
        to the last known state from the workspace API.

        Returns:
            int: The total number of instance roles available.
        """
        return super().__len__()

    def __getitem__(self, key) -> Union[IInstanceRole, List[IInstanceRole]]:
        """
        Supports accessing individual instance roles or a slice of instance roles from the list,
        handling pagination transparently. This method enables indexing and slicing
        operations.

        Args:
            key (int | slice): The index or slice indicating which instance roles to access.

        Returns:
            Union[IInstanceRole, List[IInstanceRole]]: A single instance role or a list of instance roles, depending
                on the type of key provided.

        Raises:
            IndexError: If the key is out of the bounds of the instance role list.
        """
        return super().__getitem__(key)

    def __contains__(self, obj) -> bool:
        """
        Checks if a specific instance role is present in the current list of instance roles.

        Args:
            obj: The instance role object to check for presence in the list.

        Returns:
            bool: True if the instance role is present in the list; False otherwise.
        """
        return super().__contains__(obj)

    @check_deprecation
    def delete(self) -> None:
        for i in self:
            i.delete()
