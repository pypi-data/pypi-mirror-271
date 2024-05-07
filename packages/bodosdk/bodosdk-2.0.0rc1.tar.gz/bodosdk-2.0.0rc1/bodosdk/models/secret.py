from __future__ import annotations
from typing import Optional, List, Union, Any

from pydantic import Field

from bodosdk.base import SDKBaseModel
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.exceptions import ValidationError
from bodosdk.interfaces import (
    IBodoWorkspaceClient,
    ISecretGroup,
    ISecretGroupFilter,
    ISecretGroupList,
    ISecret,
    ISecretFilter,
    ISecretList,
)


class SecretGroup(SDKBaseModel, ISecretGroup):
    """
    A class to manage secret groups within a workspace environment.

    Attributes:
        uuid (Optional[str]): Unique identifier for the secret group.
        name (Optional[str]): Name of the secret group.
        description (Optional[str]): Description of the secret group.
    """

    uuid: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        """
        Initializes a new instance of the SecretGroup class.

        Args:
            workspace_client (IBodoWorkspaceClient, optional): Client for interacting with
                the workspace API. Defaults to None.
            **data: Arbitrary keyword arguments that are passed to the base class
                and used for initializing model properties.
        """
        super().__init__(**data)
        self._workspace_client = workspace_client

    def __call__(self, **data) -> SecretGroup:
        """
        Creates a new instance of SecretGroup using the same workspace client.

        Args:
            **data: Arbitrary keyword arguments used for creating a new instance.

        Returns:
            SecretGroup: A new instance of SecretGroup.
        """
        return SecretGroup(self._workspace_client, **data)

    @check_deprecation
    def _save(self) -> SecretGroup:
        """
        Saves the current state of the SecretGroup. If the group has been modified,
        it updates the existing group if UUID is present, or creates a new group if not.

        Returns:
            SecretGroup: The updated SecretGroup instance.

        """
        if self._modified:
            if self.uuid:
                resp = self._workspace_client._secret_group_api.update_secret_group(
                    self
                )
            else:
                resp = self._workspace_client._secret_group_api.create_secret_group(
                    self
                )
            self._update(resp)
            self._modified = False
        return self

    @check_deprecation
    def delete(self):
        """
        Deletes this secret group from the workspace using the group's name.

        """
        self._workspace_client._secret_group_api.delete_secret_group(self.name)


class SecretGroupFilter(SDKBaseModel, ISecretGroupFilter):
    names: Optional[List[str]] = None


class SecretGroupList(ISecretGroupList, SDKBaseModel):
    class Config:
        extra = "forbid"
        allow_population_by_field_name = True

    page: Optional[int] = Field(0, alias="page")
    page_size: Optional[int] = Field(10, alias="pageSize")
    total: Optional[int] = Field(None, alias="total")
    order: Optional[dict] = Field(default_factory=dict, alias="order")
    filters: Optional[Union[SecretGroupFilter, dict]] = Field(None, alias="filters")

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        super().__init__(**data)
        self._elements: List[SecretGroup] = []
        self._workspace_client = workspace_client

    def __call__(self, **data) -> SecretGroupList:
        sg_list = SecretGroupList(self._workspace_client, **data)
        return sg_list._load_next_page()

    def __iter__(self) -> SecretGroup:
        yield from super().__iter__()

    def _load_next_page(self) -> SecretGroupList:
        self._mutable = True
        self.page += 1
        resp = self._workspace_client._secret_group_api.get_secret_groups(
            page=self.page,
            page_size=self.page_size,
            names=self.filters.names if self.filters else None,
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
        for elem in resp:
            sg = self._workspace_client.CatalogClient.SecretGroup(**elem)
            self._elements.append(sg)
        self.total = len(resp)
        self._mutable = False
        return self

    @check_deprecation
    def delete(self):
        for sg in self:
            sg.delete()


class Secret(SDKBaseModel, ISecret):
    """
    A class to manage secrets within a workspace environment.

    Attributes:
        uuid (Optional[str]): Unique identifier for the secret.
        name (Optional[str]): Name of the secret.
        secret_type (Optional[str]): Type of the secret (e.g., API key, password).
        data (Optional[dict]): The actual data of the secret in a dictionary.
        secret_group (Optional[Union[SecretGroup, dict]]): The secret group this secret
            belongs to, can be a SecretGroup instance or a dictionary describing the group.

    """

    uuid: Optional[str] = None
    name: Optional[str] = None
    secret_type: Optional[str] = Field(None, alias="secretType")
    data: Optional[dict] = None
    secret_group: Optional[Union[SecretGroup, dict]] = Field(None, alias="secretGroup")

    def __setattr__(self, key: str, value: Any):
        """
        Sets attribute values, with special handling for the 'secret_group' attribute.

        Args:
            key (str): Attribute name.
            value (Any): The value to be set.
        """

        if key == "secret_group" and isinstance(value, dict):
            try:
                super().__setattr__(
                    key, self._workspace_client.SecretClient.SecretGroup(**value)
                )
            except ValidationError as e:
                raise ValueError(f"Invalid data for InstanceRole: {e}")
        else:
            super().__setattr__(key, value)

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        """
        Initializes a new instance of the Secret class.

        Args:
            workspace_client (IBodoWorkspaceClient, optional): Client for interacting with
                the workspace API. Defaults to None.
            **data: Arbitrary keyword arguments that are passed to the base class
                and used for initializing model properties.
        """
        super().__init__(**data)
        self._workspace_client = workspace_client

    def __call__(self, **data) -> Secret:
        """
        Creates a new instance of Secret using the same workspace client.

        Args:
            **data: Arbitrary keyword arguments used for creating a new instance.

        Returns:
            Secret: A new instance of Secret.
        """
        return Secret(self._workspace_client, **data)

    @check_deprecation
    def _save(self) -> Secret:
        """
        Saves the current state of the Secret. If the secret has been modified,
        it updates the existing secret if UUID is present, or creates a new one if not.

        Returns:
            Secret: The updated Secret instance.
        """
        if self._modified:
            if self.uuid:
                resp = self._workspace_client._secrets_api.update_secret(self)
            else:
                resp = self._workspace_client._secrets_api.create_secret(self)
            self._update(resp)
            self._modified = False
        return self

    @check_deprecation
    def _load(self) -> Secret:
        """
        Loads the secret details from the workspace using its UUID.

        Returns:
            Secret: The Secret instance populated with the latest data.
        """
        resp = self._workspace_client._secrets_api.get_secret(self.uuid)
        self._update(resp)
        self._modified = False
        return self

    @check_deprecation
    def delete(self):
        """
        Deletes the secret from the workspace using the secret's UUID.
        """
        self._workspace_client._secrets_api.delete_secret(self.uuid)


class SecretFilter(SDKBaseModel, ISecretFilter):
    names: Optional[List[str]] = None
    secret_groups: Optional[List[str]] = None


class SecretList(SDKBaseModel, ISecretList):
    page: Optional[int]
    page_size: Optional[int]
    total: Optional[int]
    order: Optional[dict]
    filters: Optional[Union[SecretFilter, dict]]

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        super().__init__(**data)
        self._elements: List[Secret] = []
        self._workspace_client = workspace_client

    def __call__(self, **data) -> SecretList:
        secret_list = SecretList(self._workspace_client, **data)
        return secret_list._load_next_page()

    def __iter__(self) -> Secret:
        yield from super().__iter__()

    def _load_next_page(self) -> SecretList:
        self._mutable = True
        self.page += 1
        resp = self._workspace_client._secrets_api.get_all_secrets(
            page=self.page,
            page_size=self.page_size,
            names=self.filters.names if self.filters else None,
            secret_groups=self.filters.secret_groups if self.filters else None,
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
        for elem in resp:
            sg = self._workspace_client.CatalogClient.Secret(**elem)
            self._elements.append(sg)
        self.total = len(resp)
        self._mutable = False
        return self

    @check_deprecation
    def delete(self):
        for secret in self:
            secret.delete()
