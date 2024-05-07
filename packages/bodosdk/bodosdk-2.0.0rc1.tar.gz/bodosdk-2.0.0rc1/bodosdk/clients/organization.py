import os
from typing import Optional, List, Union
from unittest.mock import MagicMock

from bodosdk import _version
from bodosdk.api.auth import AuthApi
from bodosdk.api.cloud_config import CloudConfigApi
from bodosdk.api.request_wrapper import RequestWrapper
from bodosdk.api.workspace import WorkspaceApi
from bodosdk.base import APIKeys
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.exceptions import APIKeysMissing
from bodosdk.interfaces import (
    IBodoOrganizationClient,
    IAwsCloudConfig,
    IAzureCloudConfig,
)
from bodosdk.models.cloud_config import (
    CloudConfigList,
    AwsCloudConfig,
    AzureCloudConfig,
    CloudConfigBase,
)
from bodosdk.models.common import AWSNetworkData, NetworkData
from bodosdk.models.workspace import Workspace, WorkspaceList, WorkspaceFilter


class BodoOrganizationClient(IBodoOrganizationClient):
    def __init__(
        self,
        client_id=None,
        secret_key=None,
        api_url="https://api.bodo.ai/api",
        auth_url="https://auth.bodo.ai",
        print_logs=False,
    ):
        self._client_id = client_id
        self._secret_key = secret_key
        self._api_url = api_url
        self._auth_url = auth_url
        self._print_logs = print_logs
        self._workspace_data = None

        if not self._client_id:
            self._client_id = os.environ.get("BODO_ORG_CLIENT_ID")

        if not self._secret_key:
            self._secret_key = os.environ.get("BODO_ORG_SECRET_KEY")

        if not self._client_id or not self._secret_key:
            raise APIKeysMissing(
                "BODO_ORG_CLIENT_ID and BODO_ORG_SECRET_KEY environment variables "
                "should be set if APIKeys are not passed to BodoWorkspaceClient()"
            )

        auth = APIKeys(client_id=self._client_id, secret_key=self._secret_key)

        self._auth_api = AuthApi(auth, auth_url, RequestWrapper(print_logs))

        self._workspace_api = WorkspaceApi(
            self._auth_api, api_url, RequestWrapper(print_logs)
        )

        self._cloud_config_api = CloudConfigApi(
            self._auth_api, api_url, RequestWrapper(print_logs)
        )

        self._sdk_api = MagicMock()

        self._deprecated_methods = self._sdk_api.get_organization_client_info(
            _version.get_versions().get("version")
        )

    @property
    def Workspace(self) -> Workspace:
        return Workspace(org_client=self)

    @property
    def WorkspaceList(self) -> WorkspaceList:
        return WorkspaceList(org_client=self)

    @property
    def CloudConfig(self) -> CloudConfigBase:
        return CloudConfigBase(org_client=self)

    @property
    def AwsCloudConfig(self) -> AwsCloudConfig:
        return AwsCloudConfig(org_client=self)

    @property
    def AzureCloudConfig(self) -> AzureCloudConfig:
        return AzureCloudConfig(org_client=self)

    @property
    def CloudConfigList(self) -> CloudConfigList:
        return CloudConfigList(org_client=self)

    @check_deprecation
    def create_workspace(
        self,
        name: str,
        region: str,
        storage_endpoint_enabled: bool,
        cloud_config_id: str = None,
        vpc_id: Optional[str] = None,
        public_subnets_ids: Optional[List[str]] = None,
        private_subnets_ids: Optional[List[str]] = None,
        custom_tags: Optional[dict] = None,
    ) -> Workspace:
        if vpc_id:
            network_data = AWSNetworkData(
                region=region,
                storage_endpoint=storage_endpoint_enabled,
                vpc_id=vpc_id,
                public_subnets_ids=public_subnets_ids,
                private_subnets_ids=private_subnets_ids,
            )
        else:
            network_data = NetworkData(
                region=region,
                storage_endpoint=storage_endpoint_enabled,
            )
        workspace = self.Workspace(
            name=name,
            custom_tags=custom_tags,
            network_data=network_data,
            cloud_config=CloudConfigBase(uuid=cloud_config_id),
        )
        return workspace._save()

    @check_deprecation
    def get_workspace(self, id) -> Workspace:
        return self.Workspace(uuid=id)._load()

    @check_deprecation
    def delete_workspace(self, id) -> Workspace:
        return self.Workspace(uuid=id).delete()

    @check_deprecation
    def list_workspaces(
        self, filters: Optional[Union[WorkspaceFilter, dict]] = None
    ) -> WorkspaceList:
        return self.WorkspaceList(filters=filters)

    @check_deprecation
    def list_cloud_configs(
        self, filters: Optional[Union[dict]] = None
    ) -> CloudConfigList:
        return self.CloudConfigList(filters=filters)

    @check_deprecation
    def get_cloud_config(self, id) -> Union[IAwsCloudConfig, IAzureCloudConfig]:
        return self.CloudConfig(uuid=id)._load()
