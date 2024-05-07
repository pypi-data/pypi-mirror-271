import os
from unittest.mock import MagicMock

from bodosdk import _version
from bodosdk.api.auth import AuthApi
from bodosdk.api.catalog import CatalogApi
from bodosdk.api.cluster import ClusterApi
from bodosdk.api.instance_role import InstanceRoleApi
from bodosdk.api.job import JobApi
from bodosdk.api.job_tpl import JobTplApi
from bodosdk.api.request_wrapper import RequestWrapper
from bodosdk.api.secret_group import SecretGroupApi
from bodosdk.api.secrets import SecretsApi
from bodosdk.api.workspace import WorkspaceApi
from bodosdk.base import APIKeys
from bodosdk.clients.catalog import CatalogClient
from bodosdk.clients.cluster import ClusterClient
from bodosdk.clients.instance_role import InstanceRoleClient
from bodosdk.clients.job import JobClient
from bodosdk.clients.job_tpl import JobTemplateClient
from bodosdk.clients.secret import SecretClient
from bodosdk.exceptions import APIKeysMissing
from bodosdk.interfaces import (
    IBodoWorkspaceClient,
    IWorkspace,
    IJobClient,
    IJobTemplateClient,
)
from bodosdk.interfaces import IClusterClient
from bodosdk.models.workspace import Workspace


class BodoWorkspaceClient(IBodoWorkspaceClient):
    ClusterClient: IClusterClient
    JobClient: IJobClient
    JobTemplateClient: IJobTemplateClient

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
            self._client_id = os.environ.get("BODO_CLIENT_ID")

        if not self._secret_key:
            self._secret_key = os.environ.get("BODO_SECRET_KEY")

        if not self._client_id or not self._secret_key:
            raise APIKeysMissing(
                "BODO_CLIENT_ID and BODO_SECRET_KEY environment variables "
                "should be set if APIKeys are not passed to BodoWorkspaceClient()"
            )

        auth = APIKeys(client_id=self._client_id, secret_key=self._secret_key)

        self._auth_api = AuthApi(auth, auth_url, RequestWrapper(print_logs))

        self._job_api = JobApi(self._auth_api, api_url, RequestWrapper(print_logs))

        self._job_tpl_api = JobTplApi(
            self._auth_api, api_url, RequestWrapper(print_logs)
        )

        self._cluster_api = ClusterApi(
            self._auth_api, api_url, RequestWrapper(print_logs)
        )

        self._instance_api = InstanceRoleApi(
            self._auth_api, api_url, RequestWrapper(print_logs)
        )

        self._secret_group_api = SecretGroupApi(
            self._auth_api, api_url, RequestWrapper(print_logs)
        )

        self._secrets_api = SecretsApi(
            self._auth_api, api_url, RequestWrapper(print_logs)
        )

        self._catalog_api = CatalogApi(
            self._auth_api, api_url, RequestWrapper(print_logs)
        )

        self._workspace_api = WorkspaceApi(
            self._auth_api, api_url, RequestWrapper(print_logs)
        )

        self._sdk_api = MagicMock()

        self._deprecated_methods = self._sdk_api.get_workspace_client_info(
            _version.get_versions().get("version")
        )

        self.ClusterClient = ClusterClient(self)
        self.JobClient = JobClient(self)
        self.JobTemplateClient = JobTemplateClient(self)
        self.InstanceRoleClient = InstanceRoleClient(self)
        self.CatalogClient = CatalogClient(self)
        self.SecretClient = SecretClient(self)

        decoded_auth_token = self._auth_api.decode_token(self._auth_api.auth_token)
        self._workspace_uuid = decoded_auth_token.get("tenantId")

    @property
    def workspace_data(self) -> IWorkspace:
        if not self._workspace_data:
            self._workspace_data = Workspace(
                **self._workspace_api.get(self._workspace_uuid).dict()
            )
        return self._workspace_data

    @property
    def workspace_id(self) -> str:
        return self._workspace_uuid
