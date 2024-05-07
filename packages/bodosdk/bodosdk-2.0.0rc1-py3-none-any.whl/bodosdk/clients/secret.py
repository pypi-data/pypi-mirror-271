from typing import Union

from bodosdk import _version
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.interfaces import IBodoWorkspaceClient, ISecretClient
from bodosdk.models.secret import (
    SecretGroup,
    SecretGroupList,
    Secret,
    SecretList,
    SecretGroupFilter,
    SecretFilter,
)


class SecretClient(ISecretClient):
    _deprecated_methods: dict

    def __init__(self, workspace_client: IBodoWorkspaceClient):
        self._workspace_client = workspace_client
        self._check_deprecation()

    def _check_deprecation(self):
        methods = self._workspace_client._sdk_api.get_secret_client_info(
            _version.get_versions().get("version")
        )
        if isinstance(methods, dict) and methods:
            self._deprecated_methods = methods
        else:
            self._deprecated_methods = {}

    @property
    def SecretGroup(self) -> SecretGroup:
        return SecretGroup(self._workspace_client)

    @property
    def SecretGroupList(self) -> SecretGroup:
        return SecretGroupList(self._workspace_client)

    @property
    def Secret(self) -> SecretGroup:
        return Secret(self._workspace_client)

    @property
    def SecretList(self) -> SecretGroup:
        return SecretList(self._workspace_client)

    @check_deprecation
    def list_secret_groups(
        self, filters: Union[dict, SecretGroupFilter] = None
    ) -> SecretGroupList:
        return self.SecretGroupList(filters=filters)

    @check_deprecation
    def list_secrets(self, filters: Union[dict, SecretFilter] = None) -> SecretList:
        return self.SecretList(filters=filters)

    @check_deprecation
    def get_secret(
        self,
        id: str,
    ) -> Secret:
        return self.Secret(uuid=id)._load()

    @check_deprecation
    def create_secret(
        self,
        name: str,
        secret_type: str,
        data: dict,
        secret_group: SecretGroup,
    ) -> Secret:
        secret = self.Secret(
            secret_type=secret_type,
            name=name,
            data=data,
            secret_group=secret_group,
        )
        return secret._save()

    @check_deprecation
    def delete_secret(self, id: str):
        self.Secret(uuid=id).delete()

    @check_deprecation
    def create_secret_group(
        self,
        name: str,
        description: str,
    ) -> SecretGroup:
        sg = self.SecretGroup(
            name=name,
            description=description,
        )
        return sg._save()

    @check_deprecation
    def delete_secret_group(self, name: str):
        self.SecretGroup(name=name).delete()
